from twisted.internet.protocol import Factory, Protocol


class TCPClient(Protocol):
    """Client that can be used for TCP connections"""

    def send_message(self, message):
        if isinstance(message, str):
            self.transport.write(str.encode(message))
        elif isinstance(message, bytes):
            self.transport.write(message)
        else:
            raise ValueError('Invalid message, should be bytes or str.')


class TCPServer(Protocol):
    """TCP server which listens to a given port"""

    def dataReceived(self, data):
        raise NotImplementedError


class TCPFactory(Factory):
    """Factory which builds a certain TCP server connection"""

    def __init__(self, class_name, *args):
        self.class_name = class_name
        self.args = args

    def buildProtocol(self, addr):
        return self.class_name(*self.args)
