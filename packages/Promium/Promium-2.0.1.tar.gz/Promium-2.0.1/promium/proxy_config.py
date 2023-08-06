
import time
import logging
import socket
import subprocess
import re

from mitmproxy import http

from mitmproxy.proxy.server import ConnectionHandler
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster


log = logging.getLogger(__name__)
ALL_SKIPPED_HOSTS = frozenset([
    "money.yandex.ru",
    "mc.yandex.ru",
    "www.google-analytics.com",
    "www.googletagmanager.com",
    "gaua.hit.gemius.pl",
    "stats.g.doubleclick.net",
    "oauth.googleusercontent.com",
    "ssl.gstatic.com",
    "apis.google.com",
    "tpc.googlesyndication.com",
    "partner.googleadservices.com",
    "accounts.google.com",
    "track.recreativ.ru",
    "www.google.com",
    "pubads.g.doubleclick.net",
    "counter.yadro.ru",
    "www.youtube.com",
    "static-maps.yandex.ru",
    "maps.yandex.net",
    "api-maps.yandex.ru",
    "images.by-trunk.uaprom",
    "images.by-stable.uaprom",
    "images.madmax.evo",
    "images.furiosa.evo",
    "mystatus.skype.com",
    "tpc.googlesyndication.com",
    "tracker.trunk.uaprom",
    "belprom-uc.s3.amazonaws.com",
    "www.googletagservices.com",
    "demo.clerk.gitlab.uaprom",
    "clerk-demo.stg.evo",
    "static.siteheart.com",
    "code.jivosite.com",
    "cdn.callbackhunter.com",
    "vk.com",
    "connect.ok.ru",
    "cdn.pozvonim.com",
    "docviewer.yandex.ru",
    "maps.google.com",
    "maps.googleapis.com",
    "pixel.rubiconproject.com",
    "gum.criteo.com",
    "cdn.onthe.io",
    "tt.onthe.io",
    "static.criteo.net",
    "sslwidget.criteo.com",
    "creativecdn.com"
])


class AddCookieAddon():
    def __init__(self, xrequestid):
        self.xrequestid = xrequestid

    def request(self, flow):
        try:
            self._handle_request(flow)
        except Exception as e:
            log.warning(f"[Proxy] Error handling request {'-*-' * 25} {e}")

    def _handle_request(self, flow):
        cookie = ""
        extend_cookie = f"xrequestid={self.xrequestid}"
        headers = flow.request.headers

        if "Cookie" in headers:
            cookie = headers["Cookie"]
        headers["Cookie"] = (
            cookie + "; " + extend_cookie if cookie else extend_cookie
        )


class SkipperAddon():
    def __init__(self, allowed_hosts=(), skipped_hosts=()):
        self.requests = {}
        hosts = set(skipped_hosts)
        hosts.difference_update(allowed_hosts)
        self.skipped_hosts = frozenset(hosts)

    def request(self, flow):
        try:
            self._handle_request(flow)
        except Exception as e:
            log.warning(f"[Proxy] Error handling request {'-*-' * 25} {e}")

    def response(self, flow):
        try:
            self._handle_response(flow)
        except Exception as e:
            log.warning(f"[Proxy] Error handling response {'-*-' * 25} {e}")

    def _handle_request(self, flow):
        tm = time.time()
        self.requests[flow] = tm
        host = flow.request.pretty_host
        if host in self.skipped_hosts:
            resp = http.HTTPResponse.make(
                200, "",
                [(b"Content-Type", b"text/html"), (b"X-Mitm-Proxy", b'true')]
            )
            flow.response = resp

    def _handle_response(self, flow):
        tm = time.time()
        start = self.requests.pop(flow)
        duration = tm - start
        status_code = flow.response.status_code
        if status_code >= 400:
            log.warning(
                f"[Proxy] !!!!! STATUS CODE {status_code} !!!!! "
                f"{flow.request.method} {flow.request.url} "
            )
        elif duration > 10:
            log.warning(
                f"[Proxy] !!!!! SLOW REQUEST !!!!! duration={duration:.2f}sec "
                f"{flow.request}, status code {status_code}"
            )


class IntrospectionMaster(DumpMaster):
    def __init__(self, opts, server, allowed_hosts, skipped_hosts, xrequestid):
        super().__init__(opts, with_termlog=False, with_dumper=False)
        self.server = server
        self.addons.add(SkipperAddon(allowed_hosts, skipped_hosts,))
        self.addons.add(AddCookieAddon(xrequestid))

    def run(self):
        try:
            return DumpMaster.run(self)
        except Exception as e:
            self.shutdown()
            if not isinstance(e, KeyboardInterrupt):
                raise


class MyHandler(ConnectionHandler):

    def __init__(
            self,
            conn,
            addr,
            config,
            channel,
            disabled_addresses=frozenset()
    ):
        self.disabled_addresses = disabled_addresses
        ConnectionHandler.__init__(self, conn, addr, config, channel)


class MyServer(ProxyServer):

    def __init__(self, config, disabled_addresses=frozenset()):
        self.disabled_addresses = disabled_addresses
        ProxyServer.__init__(self, config)

    def handle_client_connection(self, conn, client_address):
        h = MyHandler(
            conn,
            client_address,
            self.config,
            self.channel,
            disabled_addresses=self.disabled_addresses
        )
        h.handle()


def _ip_int(ip):
    nums = map(int, ip.split('.'))
    ipint = 0
    for i in nums:
        ipint = (ipint << 8) | i
    return ipint


def _get_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


def _get_addr():
    try:
        routes_output = subprocess.check_output(['ip', 'route'])
        routes = routes_output.splitlines()
        pattern = (
            "\d{3}.\d+.\d+.\d+/(24|22) dev [a-z0-9]+ proto kernel"
            " scope link src (?P<ip>\d{3}.\d+.\d+.\d+)"
        )
        result = re.search(pattern, str(routes_output))
        if result:
            route = _ip_int(result.group("ip"))
        else:
            for line in routes:
                pieces = line.split()
                if pieces[:2] == ['default', 'via']:
                    route = _ip_int(pieces[2])
                    break
            else:
                raise RuntimeError("Can't find default route")
        addresses = subprocess.check_output(
            ['ip', 'addr']
        ).decode().splitlines()
        for line in addresses:
            pieces = line.split()
            if pieces[0] == 'inet':
                ip, cls = pieces[1].split('/')
                mask = ~((1 << (32 - int(cls))) - 1)
                if _ip_int(ip) & mask == route & mask:
                    myip = ip
                    break
        else:
            raise RuntimeError("Can't find ip address")
    except Exception as e:
        log.info(f"[Proxy] Caught Exception: {str(e)}")
        log.info("[Proxy] It can't get ip address :(")
        raise
    else:
        return myip
