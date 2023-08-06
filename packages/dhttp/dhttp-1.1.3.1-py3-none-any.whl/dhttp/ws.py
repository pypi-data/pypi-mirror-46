"""Slightly higher-level WebSocket handling class."""
import functools


class WSEntryPoint(object):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.app.websocket(*args, **kwargs)(self._handle_connection)

    def _handle_connection(self, client, req):
        client.ws_receiver(functools.partial(self.on_receive, client, req))
        self.on_connect(client, req)

    # Virtual methods
    def on_connect(self, client, req):
        pass

    def on_receive(self, client, req, packet):
        pass