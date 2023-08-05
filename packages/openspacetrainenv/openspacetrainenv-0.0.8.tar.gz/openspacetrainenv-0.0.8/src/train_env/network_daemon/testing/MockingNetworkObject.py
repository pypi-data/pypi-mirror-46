"""Module that contains test objects that allow developers to write tests for network logic"""

from abc import ABC

from twisted.internet.protocol import DatagramProtocol, Protocol
from twisted.test.proto_helpers import StringTransport

from src.network_daemon import TCPServer, TCPClient
from src.network_daemon.multicast_network_objects import NetworkServer, NetworkClient


class MockingTransport(StringTransport):
    """Mocking transport which takes strings"""


class MockingNetworkObject(DatagramProtocol):
    """Mocking network object which uses the MockingTransport"""

    def __init__(self):
        super(DatagramProtocol, self).__init__()
        self.transport = MockingTransport()


class MockingNetworkServer(MockingNetworkObject, NetworkServer):
    """Mocking network server which uses the MockingTransport"""


class MockingNetworkClient(MockingNetworkObject, NetworkClient):
    """Mocking network client which uses the MockingTransport and implements the send_message logic"""

    def send_message(self, message):
        if isinstance(message, str):
            self.transport.write(str.encode(message))
        elif isinstance(message, bytes):
            self.transport.write(message)
        else:
            raise ValueError('Invalid message, should be bytes or str.')


class MockingNetworkProtocol(Protocol):
    """Mocking class for protocols"""

    def __init__(self):
        self.transport = MockingTransport()


class MockingNetworkTCPServer(MockingNetworkProtocol, TCPServer, ABC):
    """Mocking TCP server"""

    def __init__(self):
        MockingNetworkProtocol.__init__(self)


class MockingNetworkTCPClient(MockingNetworkProtocol, TCPClient):
    """Mocking TCP client"""

    def __init__(self):
        MockingNetworkProtocol.__init__(self)
