import json
import os
import random
import unittest

import pika
import requests
from twisted.internet import reactor
from twisted.web import server
from twisted.web.http import HTTPChannel

from src import EventListener, Broker, Event
from src import OccupancyData
from src.data_container import ConfigUpdate
from src.network_daemon import MockingTransport
from src.train_unit_data_aggregator import TrainUnitDataAggregator, TransferModule, AMQPTransferModule, \
    InternalNetworkAPI
from src.train_unit_data_aggregator.testing.utils import find_free_port


class TestPlugin(EventListener):
    def __init__(self):
        super().__init__()
        self.set_message_type_callback('update_test', self.update_configuration)
        Broker().subscribe(self, 'update_test')

    def update_configuration(self, config_update):
        path = os.path.dirname(os.path.realpath(__file__)) + '/test_config.json'
        with open(path, 'w') as file:
            file.write(json.dumps(config_update.data))


class _TestTrainUnitDataAggregator(TrainUnitDataAggregator):

    def __init__(self, transfer_module=None, internal_API=None):
        tm = transfer_module
        if transfer_module is None:
            tm = _TestTransferModule()
        super().__init__(tm, internal_API, 200)
        self.received_data = None

    def receive_config_update(self, model_update):
        self.received_data = model_update
        Broker().publish(Event('update_test', model_update))

    def _local_config_update(self, config_update, basepath_plugin=''):
        super()._local_config_update(config_update, basepath_plugin)


class _TestTransferModule(TransferModule):

    def __init__(self):
        super().__init__()
        self.received_data = None

    def transfer_to_backend(self, data, queue='queue'):
        self.received_data = data


class TestTrainUnitDataAggregator(unittest.TestCase):

    def test_transfer_to_train(self):
        test_transfer_module = _TestTransferModule()
        test_occupancy = OccupancyData(55,
                                       {'1': True, '2': False, '3': True, '4': False},
                                       {'free_seats': 2, 'fill_rate': 0.5})

        # This should throw an error as the transfer module does not know its tuda
        self.assertRaises(ValueError, test_transfer_module.transfer_to_train, test_occupancy)

    def test_receive_occupancy_data(self):
        self.skipTest("The transfermodule is now called via twisted and thus uses a reactor")
        # First let the tuda know all the carriages in the train
        test_transfer_module = _TestTransferModule()
        test_tuda = _TestTrainUnitDataAggregator(test_transfer_module)

        test_tuda.receive_carriage_data(1)
        test_tuda.receive_carriage_data(2)
        test_tuda.receive_carriage_data(3)

        test_occ_1 = OccupancyData(1,
                                   {'1': True, '2': False, '3': True, '4': False},
                                   {'free_seats': 2, 'fill_rate': 0.5})
        test_occ_2 = OccupancyData(2,
                                   {'1': False, '2': False, '3': False, '4': False},
                                   {'free_seats': 4, 'fill_rate': 0})
        test_occ_3 = OccupancyData(3,
                                   {'1': True, '2': True, '3': True, '4': True},
                                   {'free_seats': 0, 'fill_rate': 1})

        # Send the occupancies one a a time and check each time if the transfer module received the occupancies.
        # The tuda should only send the occupancies to the transfer module when it received occupancy data for
        # each carriage in the train.
        test_tuda.receive_occupancy_data(test_occ_1)
        self.assertIsNone(test_transfer_module.received_data)

        # Send occupancy for a carriage that already sent its occupancy to check if the tuda does not
        # send the occupancies to the transfer module until all occupancies are available.
        test_tuda.receive_occupancy_data(test_occ_1)
        self.assertIsNone(test_transfer_module.received_data)

        test_tuda.receive_occupancy_data(test_occ_2)
        self.assertIsNone(test_transfer_module.received_data)

        test_tuda.receive_occupancy_data(test_occ_3)
        self.assertIsNotNone(test_transfer_module.received_data)

        # Check if the tuda did reset its occupancy data map after sending all the occupancies in the map
        # to the transfer module
        self.assertEqual(test_tuda._occupancy_data_map, {1: None, 2: None, 3: None})

        test_tuda.destroy()

    def test_receive_carriage_data(self):
        test_transfer_module = _TestTransferModule()
        test_tuda = _TestTrainUnitDataAggregator(test_transfer_module)
        test_tuda._occupancy_data_map = {}

        test_tuda.receive_carriage_data(1)
        test_tuda.receive_carriage_data(2)
        test_tuda.receive_carriage_data(2)

        # The tuda should know that there are 3 carriages in the train
        expected_occupancy_map = {1: None, 2: None}
        self.assertEqual(test_tuda._occupancy_data_map, expected_occupancy_map)

        expected_occupancy_map = {1: None, 2: None, 3: None}
        test_tuda.receive_carriage_data(3)
        self.assertEqual(test_tuda._occupancy_data_map, expected_occupancy_map)

        test_tuda.clear_carriages()
        expected_occupancy_map = {test_tuda.carriage_id: None}
        self.assertEqual(test_tuda._occupancy_data_map, expected_occupancy_map)

        test_tuda.destroy()


    def test_receive_model_update(self):
        test_transfer_module = _TestTransferModule()
        test_tuda = _TestTrainUnitDataAggregator(test_transfer_module)
        test_model_update = ConfigUpdate(0, 'test_data', 'test')
        test_model_update.timestamp = 0

        # Send a dummy model update to the tuda
        test_transfer_module.transfer_to_train({"carriage_id": 0, "config_type": "test_data", "data": "test"})

        # Check if the tuda received the model update from the transfer module
        test_tuda.received_data.timestamp = 0
        self.assertEqual(test_tuda.received_data, test_model_update)

        test_tuda.destroy()

    def test_handle_network_request(self):
        api = InternalNetworkAPI(port=find_free_port())
        test_tuda = _TestTrainUnitDataAggregator(internal_API=api)
        test_occupancy = OccupancyData(55,
                                       {'1': True, '2': False, '3': True, '4': False},
                                       {'free_seats': 2, 'fill_rate': 0.5})

        # Send the occupancy to the tuda who should forward it to the internal API
        test_tuda.receive_occupancy_data(test_occupancy)
        channel = HTTPChannel()
        transport = MockingTransport()
        channel.transport = transport
        request = server.Request(channel)
        request.path = b"/occupancy"
        response = json.loads(test_tuda.internal_API.render_GET(request).decode("utf-8"))

        # Request the occupancy using a valid path: /occupancy
        response = json.loads(api.render_GET(request).decode("utf-8"))
        self.assertCountEqual(response, [test_occupancy.to_API_object()])

        path = "^/test$"
        test_tuda.internal_API.add_path(path, lambda x: None)
        self.assertTrue(path in test_tuda.internal_API.path_handlers)
        test_tuda.internal_API.remove_path(path)
        self.assertTrue(path not in test_tuda.internal_API.path_handlers)

        test_tuda.destroy()

    def test_transfer_module_AMQP(self):
        self.skipTest("This test uses a reactor and should thus be ran as a standalone test.")
        try:
            test_message = "testmessage"
            # check if connection available
            requests.get("https://www.google.com/")
            tm = AMQPTransferModule(amqp_host="193.190.127.224", username="admin", password="openspace")
            tm.transfer_to_backend(test_message, "test")
            reactor.callLater(0.5, reactor.stop)
            reactor.run()
            connection = pika.BlockingConnection(pika.ConnectionParameters("193.190.127.224", 5672, "/",
                                                                           pika.PlainCredentials("admin", "openspace")))
            channel = connection.channel()
            channel.queue_declare(queue="test")
            method_frame, header_frame, body = channel.basic_get(queue='test', no_ack=True)
            channel.close()
            connection.close()
            self.assertEqual(body.decode("utf-8")[1:-1], test_message)

        except requests.exceptions.ConnectionError:
            self.skipTest("No connection available for execution of this test")

    class _TestConnection:
        def __init__(self):
            self.open = True

        def close(self):
            self.open = False

    def test_transfer_module_AMQP_utils(self):
        from src import Logger
        import time

        r_val = random.random()
        error_string = f"Got error {r_val}"

        tm = AMQPTransferModule(amqp_port=9070)
        tm._on_connection_error(ValueError(error_string))

        time.sleep(0.5)

        with open(Logger().file_path) as f:
            lines = f.readlines()
            self.assertTrue(any([error_string in line for line in lines]))

        connection = self._TestConnection()
        channel = self._TestConnection()

        self.assertTrue(connection.open)
        self.assertTrue(channel.open)

        tm._reset_module(channel, connection)

        self.assertFalse(connection.open)
        self.assertFalse(channel.open)

    def test_update_configs(self):
        # initialisation
        dir_path = os.path.dirname(os.path.realpath(__file__))
        transfer_module = _TestTransferModule()
        tuda = _TestTrainUnitDataAggregator(transfer_module)
        transfer_module.attach_tuda(tuda)

        test_data = {
            "config_type": "test",
            "carriage_id": 200,
            "data": {
                "camera_handler": {
                    "mapping": {"1": "localhost"},
                    "camera_interval_delay": 60
                }
            }
        }
        TestPlugin()
        transfer_module.transfer_to_train(test_data)

        with open(dir_path + '/test_config.json', 'r') as file:
            config = file.read()
            self.assertEqual(config, json.dumps(test_data['data']))
        os.remove(dir_path + '/test_config.json')
