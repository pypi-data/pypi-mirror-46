import json
import unittest

from twisted.web import server
from twisted.web._responses import NOT_FOUND
from twisted.web.http import HTTPChannel

from src import OccupancyData
from src.network_daemon import MockingTransport
from src.train_unit_data_aggregator import InternalNetworkAPI
from src.train_unit_data_aggregator.testing.utils import find_free_port


class TestInternalNetworkAPI(unittest.TestCase):

    def test_handle_bad_path_request(self):
        api = InternalNetworkAPI(port=find_free_port())

        # Send the internal network API a request containing an path that does not exist and
        # is therefore unable to handle the request

        # Create Request
        channel = HTTPChannel()
        transport = MockingTransport()
        channel.transport = transport
        request = server.Request(channel)
        request.path = b"/this/is/a/bad/request"

        response = api.render_GET(request)

        self.assertEqual(response.code, NOT_FOUND)

    def test_handle_good_request(self):
        api = InternalNetworkAPI(port=find_free_port())

        # Create Request
        channel = HTTPChannel()
        transport = MockingTransport()
        channel.transport = transport
        request = server.Request(channel)
        request.path = b"/occupancy"

        response = json.loads(api.render_GET(request).decode("utf-8"))

        self.assertEqual(response, [])

        test_occ_1 = OccupancyData(55,
                                   {'1': True, '2': False, '3': True, '4': False},
                                   {'free_seats': 2, 'fill_rate': 0.5})
        api.receive_occupancy_data(test_occ_1)
        test_occ_2 = OccupancyData(56,
                                   {'1': True, '2': False, '3': True, '4': True},
                                   {'free_seats': 1, 'fill_rate': 0.75})
        api.receive_occupancy_data(test_occ_2)

        # Request the occupancy using a valid path: /occupancy
        response = json.loads(api.render_GET(request).decode("utf-8"))
        self.assertCountEqual(response, [test_occ_1.to_API_object(), test_occ_2.to_API_object()])

        # Add another carriage with the same ID as the first carriage in order to test if the data stored
        # in the internal API is correctly updated
        test_occ_3 = OccupancyData(55,
                                         {'1': True, '2': True, '3': True, '4': True},
                                         {'free_seats': 0, 'fill_rate': 1})
        api.receive_occupancy_data(test_occ_3)

        response = json.loads(api.render_GET(request).decode("utf-8"))
        self.assertCountEqual(response, [test_occ_3.to_API_object(), test_occ_2.to_API_object()])

        api.destroy()
