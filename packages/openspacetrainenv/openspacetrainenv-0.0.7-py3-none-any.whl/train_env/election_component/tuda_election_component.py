from twisted.internet import task

from src import ConfigurationStore, Broker, EventListener, Event
from src.election_component import NetworkElectionComponent
from src.logger import Logger
from src.train_unit_data_aggregator import InternalNetworkAPI
from src.train_unit_data_aggregator.amqp_transfer_module import AMQPTransferModule
from src.train_unit_data_aggregator.network_train_unit_data_aggregator import NetworkTrainUnitDataAggregator
from src.virtual_tuda import VirtualNetworkTUDA


class TudaElectionComponent(NetworkElectionComponent, EventListener):
    """Election component that creates a (V)TUDA when the election is done"""

    def __init__(self, with_timer=True):
        store = ConfigurationStore()
        group = store.get_value('election_mgroup')
        port = store.get_value('election_mport')

        NetworkElectionComponent.__init__(
            self, group, port, election_id=store.get_value('carriage_id'), ip=store.get_value('ip')
        )

        EventListener.__init__(self)

        self._tuda_object = None

        Broker().subscribe(self)

        self.election_deferred = None

        if with_timer:
            self.start_election_timer()

    def on_connection_failure(self):
        self.start_election()

    def on_elected(self, is_leader):
        cstore = ConfigurationStore()
        if self._tuda_object is not None:
            self._tuda_object.destroy()
        if is_leader:
            self._tuda_object = NetworkTrainUnitDataAggregator(
                cstore.get_value('tuda_ip'),
                cstore.get_value('tuda_port'),
                cstore.get_value('tuda_mgroup'),
                cstore.get_value('tuda_mport'),
                internal_api=InternalNetworkAPI(cstore.get_value('api_port')),
                transfer_module=AMQPTransferModule(
                    amqp_host=cstore.get_value('amqp_host'),
                    username=cstore.get_value('username'),
                    password=cstore.get_value('password')
                )
            )

            # Let the train unit data aggregator know which carriages are active in the train
            self._tuda_object.clear_carriages()
            discovered_carriage_ids = [carriage_id._id for carriage_id in self._others] + [self._id]
            for carriage_id in discovered_carriage_ids:
                self._tuda_object.receive_carriage_data(carriage_id)

        else:
            leader = self.get_leader()
            self._tuda_object = VirtualNetworkTUDA(
                NetworkTrainUnitDataAggregator(
                    leader.ip[0],
                    cstore.get_value('tuda_port'),
                    cstore.get_value('tuda_mgroup'),
                    cstore.get_value('tuda_mport')
                ),
                self.get_id(),
                cstore.get_value('tuda_mgroup'),
                cstore.get_value('tuda_mport')
            )

        Logger().info(
            f'Elected carriage: {self.get_leader().get_id() if not is_leader else self.get_id()}',
            location=self.__class__.__name__
        )
        Broker().publish(OnElectedEvent(self._tuda_object))

    def get_tuda_object(self):
        return self._tuda_object

    def receive_message(self, message, round_nr):
        if self.election_deferred is not None:
            self.election_deferred.reset()
        super().receive_message(message, round_nr)

    def start_election_timer(self):
        l = task.LoopingCall(self.start_election)
        l.start(ConfigurationStore().get_value('election_timer_timeout'), now=False)
        self.election_deferred = l


class OnElectedEvent(Event):
    def __init__(self, message):
        super().__init__('on_elected', message)
