import json
import re

from twisted.internet import reactor
from twisted.web import resource, server
from twisted.web.resource import NoResource

from src.train_unit_data_aggregator import InternalAPI


class InternalNetworkAPI(resource.Resource, InternalAPI):
    """
    An object of this class represents a server listening for HTTP requests received by the network of the train.
    """

    isLeaf = True

    def __init__(self, port):
        resource.Resource.__init__(self)
        InternalAPI.__init__(self)

        self.path_handlers = {"^/occupancy$": self.handle_GET_occupancy}
        self.server = server.Site(self)
        self.port = port

        self.http_listener = reactor.listenTCP(self.port, self.server)

    def destroy(self):
        if self.http_listener is not None:
            self.http_listener.loseConnection()
            self.http_listener.connectionLost(reason=None)

    def render_GET(self, request):
        handler = self._resolve_path_handler(request.path.decode("utf-8"))
        if handler is not None:
            response = handler()
        else:
            return NoResource()
        request.responseHeaders.addRawHeader(b"content-type", b"application/json")
        return response.encode("utf-8")

    def _resolve_path_handler(self, path):
        """
        Check if the requested path is defined for this server.
        If the path is known then return the correct handler to resolve the request.
        """

        for path_match, handler in self.path_handlers.items():
            if re.search(path_match, path):
                return handler
        return None

    def handle_GET_occupancy(self):
        # /occupancy
        return json.dumps([occ for occ in self.occupancy_data_map.values()])

    def add_path(self, path, callback):
        self.path_handlers[path] = callback

    def remove_path(self, path):
        self.path_handlers.pop(path)

