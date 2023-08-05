from twisted.internet.protocol import DatagramProtocol


class MulticastObject(DatagramProtocol):
    """A multicast twisted object which uses a multicast group and a port"""

    def __init__(self, group, port):
        self.group = group
        self.port = port

    def startProtocol(self):
        """Start the protocol by joining the given multicast group"""
        self.transport.joinGroup(self.group)

    def stopProtocol(self):
        if self.transport is not None:
            self.transport.loseConnection()


class NetworkServer:
    """Network server interface"""

    def datagramReceived(self, datagram, address):
        """Do something when a datagram has been received. Override this."""
        raise NotImplementedError()


class MulticastNetworkServer(MulticastObject, NetworkServer):
    """Multicast server which listens to a multicast group"""
    pass


class NetworkClient(DatagramProtocol):
    def send_message(self, message):
        if isinstance(message, str):
            self.transport.write(str.encode(message), (self.group, self.port))
        elif isinstance(message, bytes):
            self.transport.write(message, (self.group, self.port))
        else:
            raise ValueError('Invalid message, should be bytes or str.')


class MulticastNetworkClient(MulticastObject, NetworkClient):
    """Multicast client which is able to send messages"""
    pass
