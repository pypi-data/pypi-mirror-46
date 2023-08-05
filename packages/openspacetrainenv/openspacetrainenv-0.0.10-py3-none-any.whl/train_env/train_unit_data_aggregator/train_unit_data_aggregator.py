import json

from twisted.internet import reactor

from src import ConfigurationStore
from src.broker.broker import Broker, EventListener, Event
from src.logger import Logger
from src.train_unit_data_aggregator.internal_api import InternalAPI
from src.train_unit_data_aggregator.transfer_module import TransferModule

BASEPATH_PLUGINS = 'plugin'

class TrainUnitDataAggregator(EventListener):
    """
    This component is used as a central gathering point for all data from each carriage.
    The gathered data is used by the internal API and the transfer module. This component also forwards
    data received from the transfer module to the carriages.
    """

    def __init__(self, transfer_module=None, internal_api=None, carriage_id=None):
        super().__init__()
        self.internal_API = internal_api if internal_api is not None else InternalAPI()
        self.transfer_module = transfer_module if transfer_module is not None else TransferModule()
        self.carriage_id = ConfigurationStore().get_value('carriage_id') if carriage_id is None else carriage_id
        self._occupancy_data_map = {self.carriage_id: None}

        self.broker = Broker()
        self.add_broker_subscription("processed_occupancy", self.receive_occupancy_data)
        self.add_broker_subscription("update_confirmation", self.receive_update_confirmation)

        if self.transfer_module.tuda is None:
            self.transfer_module.attach_tuda(self)

    def destroy(self):
        """Method that handles cleanup of listeners amongst other things."""
        self.broker.unsubscribe(self, *self.get_callback_map().keys())

    def add_broker_subscription(self, message_type, callback):
        self.broker.subscribe(self, message_type)
        self.set_message_type_callback(message_type, callback)

    def receive_occupancy_data(self, occupancy_data):
        """"
        Receive and store seat occupancy data from a train carriage and forward it to the internal API.
        Send the occupancies to the backend whenever there is occupancy data available for each carriage in the train.
        """
        Logger().info('Received value @ TUDA', location=self.__class__.__name__)
        self.internal_API.receive_occupancy_data(occupancy_data)
        self._occupancy_data_map[occupancy_data.carriage_id] = occupancy_data
        self._forward_occupancy_data()

    def _forward_occupancy_data(self):
        """
        Send the entire occupancy data of the entire train to the backend when the occupancy from each carriage in
        the train is known and reset the occupancy data map after sending the occupancies.
        """

        missing_occupancies = sum([occ is None for occ in self._occupancy_data_map.values()])
        if missing_occupancies == 0:
            occupancies = [occ.to_API_object() for occ in self._occupancy_data_map.values()]
            # Send and reset
            reactor.callFromThread(self.transfer_module.transfer_to_backend, {"occupancy": occupancies}, 'occupancy')
            self._occupancy_data_map = {carriage_id: None for carriage_id in self._occupancy_data_map.keys()}

    def receive_update_confirmation(self, confirmation):
        reactor.callFromThread(self.transfer_module.transfer_to_backend, confirmation.to_API_object(),
                               'update_confirmation')

    def receive_carriage_data(self, carriage_id):
        """
        Receive the carriage ID from a train carriage and store this ID in the occupancy data map in order to known
        all carriages in this train. The tuda should only receive carriage data when an election
        procedure is taking place (= when all carriages of the train are being discovered).
        """

        if carriage_id not in self._occupancy_data_map.keys():
            self._occupancy_data_map[carriage_id] = None

    def _local_config_update(self, config_update, basepath_plugin = '../plugin'):
        """Send the model update to the local broker."""
        if config_update.config_type is not 'main':
            Broker().publish(Event('update_' + config_update.config_type, config_update))
        else:
                with open('main_config.json', 'w') as file:
                    file.write(json.dumps(config_update.data))

    def _global_config_update(self, config_update):
        """Send the model to the virtual train unit data aggregators on the local network"""

        pass

    def receive_config_update(self, config_update):
        """Receive a model update from the backend and forward it to each train carriage connected to the network."""

        if config_update.carriage_id == self.carriage_id:
            self._local_config_update(config_update)
        else:
            self._global_config_update(config_update)

    def clear_carriages(self):
        """Delete the known carriage IDs and this should only be done when a new election is finished."""
        self._occupancy_data_map = {self.carriage_id: None}

    def get_carriages(self):
        return self._occupancy_data_map.keys()
