import unittest

from twisted.test import proto_helpers

from src.network_daemon import MockingNetworkServer, MockingNetworkClient, MockingTransport, TCPClient, \
    MulticastNetworkServer


class _TestReceiver(MulticastNetworkServer):
    """Receiver to check if the datagrams have been received."""

    def __init__(self, group, port):
        super().__init__(group, port)
        self.received_datagrams = []

    def datagramReceived(self, datagram, address):
        self.received_datagrams.append(datagram)

    def startProtocol(self):
        pass


class TestMulticastNetwork(unittest.TestCase):

    def setUp(self):
        self.tr = proto_helpers.StringTransport()
        self.proto = _TestReceiver("224.0.0.1", 8005)
        self.proto.makeConnection(self.tr)

    def test_client(self, expected='test'):
        self.proto.datagramReceived(expected, ("224.0.0.1", 8005))
        self.assertListEqual(self.proto.received_datagrams, [expected])
        self.proto.datagramReceived(expected, ("224.0.0.1", 8005))
        self.assertListEqual(self.proto.received_datagrams, [expected, expected])

        self.proto.stopProtocol()
        self.tr.abortConnection()


class _TestMockupServer(MockingNetworkServer):
    """Mockup server that stores all received datagrams in a list."""

    def __init__(self):
        MockingNetworkServer.__init__(self)
        self.received_messages = []

    def datagramReceived(self, datagram, addr):
        if isinstance(datagram, bytes):
            self.received_messages += [datagram.decode('utf-8')]
        else:
            self.received_messages += [datagram]


class TestMockupObjects(unittest.TestCase):
    def test_mockup_network_object(self):
        expected = 'test'
        mock_server = _TestMockupServer()
        self.assertTrue(isinstance(mock_server.transport, MockingTransport))
        mock_client = MockingNetworkClient()
        mock_client.send_message(expected)
        mock_server.datagramReceived(mock_client.transport.value(), 'test')
        self.assertEqual(mock_client.transport.value().decode('utf-8'), expected)
        self.assertEqual(mock_server.received_messages[0], expected)
        mock_client.transport.clear()
        mock_client.send_message(str.encode(expected))
        mock_server.datagramReceived(mock_client.transport.value(), 'test')
        self.assertEqual(mock_server.received_messages[0], expected)


class TestTCPObjects(unittest.TestCase):
    def test_tcp_client(self):
        client = TCPClient()
        client.transport = MockingTransport()
        expected = 'test'
        client.send_message(expected)
        self.assertEqual(client.transport.value().decode('utf-8'), expected)
        client.transport.clear()
        client.send_message(str.encode(expected))
        self.assertEqual(client.transport.value().decode('utf-8'), expected)
        client.transport.clear()
        with self.assertRaises(ValueError):
            client.send_message(12)
