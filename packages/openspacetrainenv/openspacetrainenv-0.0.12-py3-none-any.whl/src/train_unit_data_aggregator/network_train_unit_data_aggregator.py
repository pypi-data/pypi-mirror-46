import json

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from src.data_container.data_container import DataTypes, OccupancyData
from src.logger import Logger
from src.network_daemon import TCPFactory, TCPServer, MulticastNetworkClient
from src.train_unit_data_aggregator import TrainUnitDataAggregator


class NetworkTrainUnitDataAggregator(TrainUnitDataAggregator):
    def __init__(self, ip, port, m_group, m_port, **kwargs):
        super().__init__(**kwargs)
        self.ip = ip
        self.port = port

        self.endpoint_listener = None
        self.delete_endpoint = False

        endpoint = TCP4ServerEndpoint(reactor, self.port)
        factory = TCPFactory(self.TUDAServer, self)
        endpoint.listen(factory).addCallback(self.set_endpoint_listener)

        self.multicast_server = MulticastNetworkClient(m_group, m_port)
        self.m_listener = reactor.listenMulticast(m_port, self.multicast_server, listenMultiple=True)

    def set_endpoint_listener(self, listener):
        self.endpoint_listener = listener
        if self.delete_endpoint:
            self.destroy()

    def destroy(self):
        super().destroy()
        Logger().debug('Disconnected listeners')
        if self.endpoint_listener is not None:
            self.endpoint_listener.loseConnection()
            self.endpoint_listener.connectionLost(reason=None)
        else:
            self.delete_endpoint = True
        if self.m_listener is not None:
            self.m_listener.stopListening()
        self.internal_API.destroy()

    class TUDAServer(TCPServer):
        data_type_callbacks = {
            DataTypes().get_value(OccupancyData): 'receive_occupancy_data'
        }

        def __init__(self, tuda: TrainUnitDataAggregator):
            self.tuda = tuda

        def dataReceived(self, data):
            message = json.loads(data)
            getattr(self.tuda, self.data_type_callbacks[message['data_type']])(message)

    def _global_config_update(self, model_update):
        self.multicast_server.send_message(model_update)

    def add_data_callback(self, datatype: DataTypes, callback):
        self.TUDAServer.data_type_callbacks[datatype] = callback
