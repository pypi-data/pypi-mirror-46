import json
import unittest

from twisted.internet import defer

from src import DataTypes, OccupancyData
from src.data_container import ConfigUpdate
from src.network_daemon.testing.MockingNetworkObject import MockingNetworkTCPClient
from src.train_unit_data_aggregator import TrainUnitDataAggregator
from src.train_unit_data_aggregator.network_train_unit_data_aggregator import NetworkTrainUnitDataAggregator
from src.virtual_tuda import VirtualTUDA, VirtualNetworkTUDA


class _TestTUDA(TrainUnitDataAggregator):
    """TUDA class used to store occupancy data for testing purposes"""

    def __init__(self):
        super().__init__()
        self.receive_buffer = []

    def receive_occupancy_data(self, occupancy_data):
        """[Overridden] Store the received occupancy data in this class"""
        self.receive_buffer.append(occupancy_data)


class TestVirtualTUDA(unittest.TestCase):
    """Test the virtual TUDA implementation without any network logic"""

    def test_simple_forward(self):
        # Create the objects
        real_tuda = _TestTUDA()
        vtuda = VirtualTUDA(real_tuda)

        # Forward occupancy data
        vtuda.forward_occupancy_data('test_occupancy')
        self.assertTrue('test_occupancy' in real_tuda.receive_buffer)


class _TestNetworkTrainUnitDataAggregator(NetworkTrainUnitDataAggregator):
    """Class that implements the TUDA network logic and stores the received objects for testing purposes"""

    def __init__(self, ip, port, **kwargs):
        super().__init__(ip, port, '228.0.0.5', 9997, **kwargs)
        self.received_occupancy = []

    def receive_occupancy_data(self, occupancy_data):
        """[Overridden] Store the received occupancy data in this class"""
        self.received_occupancy += [occupancy_data]

class _TestNetworkVirtualTuda(VirtualNetworkTUDA):
    """Class that implements the virtual TUDA network logic and stores the received objects for testing purposes"""

    def __init__(self, leader: NetworkTrainUnitDataAggregator, name):
        super().__init__(leader, name)
        self.received_model_updates = []

    def _local_config_update(self, model_update):
        """[Overridden] Store the model updates in this class"""
        self.received_model_updates += [model_update]


class TestNetworkVirtualTUDA(unittest.TestCase):
    """
    Use the network implementations to test the responsibilities of the networked, virtual and non-virtual TUDA
    These tests should not be run under a test suite as each test creates a reactor! Each test has to be run separately
    and act more as a proof that the solution also works on a network (even though it's the localhost network).
    """

    def _send_info(self, data1, data2, real_tuda):
        # Create Vtuda's
        vtuda = VirtualNetworkTUDA(real_tuda, '127.0.0.1')
        vtuda2 = VirtualNetworkTUDA(real_tuda, '127.0.0.1')

        # Forward the occupancies
        vtuda.forward_occupancy_data(data1)
        vtuda2.forward_occupancy_data(data2)

    def test_vtuda_communication(self):
        from twisted.internet import reactor

        self.skipTest('This test uses a reactor and should thus be ran as a standalone test.')

        # Create the TUDA
        real_tuda = _TestNetworkTrainUnitDataAggregator('127.0.0.1', 9991)

        # Create the occupancy data
        data1 = {'1': False, 'data_type': DataTypes().get_value(OccupancyData)}
        data2 = {'2': False, 'data_type': DataTypes().get_value(OccupancyData)}

        # Add the callbacks to the twisted reactor and let it run
        reactor.callLater(0.1, reactor.stop)
        reactor.callFromThread(self._send_info, data1, data2, real_tuda)
        reactor.run()

        # Check if the values are correct
        # Order can be random due to the network!
        self.assertCountEqual([data1, data2], real_tuda.received_occupancy)

    def _send_info_from_tuda(self, data1, data2, real_tuda):
        real_tuda.receive_config_update(json.dumps(data1))
        real_tuda.receive_config_update(json.dumps(data2))

    def test_tuda_communication(self):
        from twisted.internet import reactor

        self.skipTest('This test uses a reactor and should thus be ran as a standalone test.')

        # Create the (virtual) TUDA's
        real_tuda = _TestNetworkTrainUnitDataAggregator('127.0.0.1', 9992)
        vtuda = _TestNetworkVirtualTuda(real_tuda, '127.0.0.1')
        vtuda2 = _TestNetworkVirtualTuda(real_tuda, '127.0.0.1')

        # Create the model update data
        data1 = {'1': False}
        data2 = {'2': False}

        # Add the callbacks to the twisted reactor and let it run
        reactor.callLater(0.5, reactor.stop)
        reactor.callFromThread(self._send_info_from_tuda, data1, data2, real_tuda)
        reactor.run()

        # Check if the values are correct
        # Order can be random due to the network!
        self.assertCountEqual(vtuda.received_model_updates, [data1, data2])
        self.assertCountEqual(vtuda2.received_model_updates, [data1, data2])


class _TestMockedNetworkTrainUnitDataAggregator(_TestNetworkTrainUnitDataAggregator):
    """
    Class that implements the TUDA network logic using the network mocking objects
    and stores the received objects for testing purposes
    """

    def __init__(self, ip, port, **kwargs):
        super().__init__(ip, port, **kwargs)
        self.received_occupancy = []
        self.server = self.TUDAServer(self)
        self.others = []

    def receive_occupancy_data(self, occupancy_data):
        """[Overridden] Store the occupancy data in this class"""
        self.received_occupancy += [occupancy_data]

    def _global_config_update(self, model_update):
        """[Overridden] Send the data to all other virtual TUDA's in the network (mimicked by a list here)"""
        for other in self.others:
            other.multicast_server.datagramReceived(model_update.marshal(), None)


class _TestMockedNetworkVTUDA(VirtualNetworkTUDA):
    """
    Class that implements the virtual TUDA network logic using the network mocking objects
    and stores the received objects for testing purposes
    """

    def __init__(self, leader: NetworkTrainUnitDataAggregator, name):
        super().__init__(leader, name, '228.0.0.5', 9997)
        self.received_model_updates = []

    def open_tcp(self):
        """[Overridden] Open connection to a mocked up TCP client"""
        d = defer.Deferred()
        d.callback(MockingNetworkTCPClient())
        return d

    def _send_message(self, endpoint, message):
        """[Overridden] Send a message to a given endpoint (which is the leader)"""
        self.leader.server.dataReceived(json.dumps(message))

    def _local_config_update(self, config_update, basepath_plugin='../plugin'):
        """[Overridden] Store the model update in this class"""
        self.received_model_updates += [ConfigUpdate(
            config_update['carriage_id'],
            config_update['config_type'],
            config_update['data'],
            timestamp=config_update['timestamp']
        )]



class TestMockedNetworkVirtualTUDA(unittest.TestCase):
    """Use the mocked implementations to test the responsibilities of the networked, virtual and non-virtual TUDA"""

    def test_vtuda_communication(self):
        # Create the (virtual) TUDA's
        real_tuda = _TestMockedNetworkTrainUnitDataAggregator('127.0.0.1', 9993)
        vtuda = _TestMockedNetworkVTUDA(real_tuda, '127.0.0.1')
        vtuda2 = _TestMockedNetworkVTUDA(real_tuda, '127.0.0.1')

        # Create the occupancy data
        data1 = {'1': False, 'data_type': DataTypes().get_value(OccupancyData)}
        data2 = {'2': False, 'data_type': DataTypes().get_value(OccupancyData)}

        # Forward the first occupancy and check the result
        vtuda.forward_occupancy_data(data1)
        self.assertListEqual([data1], real_tuda.received_occupancy)

        # Forward the second occupancy and check the result
        vtuda2.forward_occupancy_data(data2)
        self.assertListEqual([data1, data2], real_tuda.received_occupancy)

        # Try another random number of forwards and check
        for i in range(10):
            vtuda2.forward_occupancy_data(data2)
        self.assertListEqual([data1, data2] + ([data2] * 10), real_tuda.received_occupancy)

    def test_tuda_to_vtuda_communication(self):
        # Create the (virtual) TUDA's
        real_tuda = _TestMockedNetworkTrainUnitDataAggregator('127.0.0.1', 9994)
        vtuda = _TestMockedNetworkVTUDA(real_tuda, '127.0.0.1')
        vtuda2 = _TestMockedNetworkVTUDA(real_tuda, '127.0.0.1')

        # Create the model update data
        data1 = ConfigUpdate(0, 'test_data', 'test')
        data2 = ConfigUpdate(0, 'test_data', 'tast')

        # Add the virtual TUDA's to the real TUDA (only for testing purposes)
        # This mimics a multicast network
        real_tuda.others = [vtuda, vtuda2]

        # Receive and forward both model updates
        real_tuda.receive_config_update(data1)
        real_tuda.receive_config_update(data2)

        # Check the values in each virtual TUDA
        self.assertListEqual([data1, data2], vtuda.received_model_updates)
        self.assertListEqual([data1, data2], vtuda2.received_model_updates)
