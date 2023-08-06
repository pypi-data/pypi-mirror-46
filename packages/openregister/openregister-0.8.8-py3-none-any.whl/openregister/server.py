from sanic import Sanic, response
import urllib.parse
from .views import DataView, favicon
from .config import DEFAULT_CONFIG


class RegisterServer:
    def __init__(self, config=None, register=None):
        self._config = dict(DEFAULT_CONFIG, **(config or {}))

    def absolute_url(self, request, path):
        url = urllib.parse.urljoin(request.url, path)
        if url.startswith("http://") and self.config("force_https"):
            url = "https://" + url[len("http://") :]
        return url

    def config_view(self):
        return DataView.as_view(self, "config.json", lambda: self._config)

    def server(self):
        server = Sanic(__name__)

        server.add_route(favicon, "/favicon.ico")
        server.add_route(self.config_view(), r"/config<suffix:(\.json)?$>")

        return server
