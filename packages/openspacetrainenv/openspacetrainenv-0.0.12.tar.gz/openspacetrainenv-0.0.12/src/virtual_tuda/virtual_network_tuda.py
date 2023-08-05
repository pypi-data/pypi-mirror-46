import json

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from src.network_daemon import TCPClient, MulticastNetworkServer
from src.train_unit_data_aggregator.network_train_unit_data_aggregator import NetworkTrainUnitDataAggregator
from src.virtual_tuda.virtual_tuda import VirtualTUDA


class VirtualNetworkTUDA(VirtualTUDA):
    """Virtual train unit data aggregator which connects to the real one using the network"""

    class VTudaMulticastNetworkServer(MulticastNetworkServer):
        """Multicast server to receive information from the train unit data aggregator"""

        def __init__(self, vtuda, group, port):
            super().__init__(group, port)
            self.vtuda = vtuda

        def datagramReceived(self, datagram, addr):
            data = json.loads(datagram)
            self.vtuda.receive_config_update(data)

    def __init__(self, leader: NetworkTrainUnitDataAggregator, name, m_group, m_port):
        super().__init__(leader)
        self.name = name
        self.multicast_server = self.VTudaMulticastNetworkServer(self, m_group, m_port)
        self.m_listener = reactor.listenMulticast(m_port, self.multicast_server, listenMultiple=True)

    def destroy(self):
        if self.m_listener is not None:
            self.m_listener.stopListening()
        self.leader.destroy()

    def open_tcp(self):
        point = TCP4ClientEndpoint(reactor, self.leader.ip, self.leader.port)
        d = connectProtocol(point, TCPClient())
        return d

    def _send_message(self, endpoint, message):
        endpoint.send_message(json.dumps(message))

    def forward_occupancy_data(self, occupancy_data):
        """Forward the occupancy data to the real TUDA."""
        d = self.open_tcp()
        d.addCallback(lambda x: self._send_message(x, occupancy_data))
        return d

    def receive_config_update(self, model_update):
        super(VirtualNetworkTUDA, self).receive_config_update(model_update)
