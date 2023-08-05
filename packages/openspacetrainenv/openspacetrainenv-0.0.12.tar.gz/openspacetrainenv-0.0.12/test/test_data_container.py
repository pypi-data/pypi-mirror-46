import os
import unittest

import cv2

from plugin.camera_handler import Frame, CameraFootage
from src import DataContainer, OccupancyData
from src.data_container import ConfigUpdate, CarriageData


class TestDataContainer(unittest.TestCase):

    def test_create_occupancy_container(self):
        carriage_id = 5
        seat_map = {'1': True, '2': False, '3': True, '4': False}
        free_seats, fill_rate = 2, 0.5
        test_occupancy = OccupancyData(carriage_id, seat_map, {'free_seats': free_seats, 'fill_rate': fill_rate})

        # Check if the container has all the right data
        self.assertEqual(test_occupancy.carriage_id, carriage_id)
        self.assertEqual(test_occupancy.seat_map, seat_map)
        self.assertEqual(test_occupancy.processed_data['free_seats'], free_seats)
        self.assertEqual(test_occupancy.processed_data['fill_rate'], fill_rate)
        self.assertIsNotNone(test_occupancy.timestamp)

    def test_create_camera_footage_container(self, img_file='testfiles/images/SampleImage.png'):
        from plugin.camera_handler import CameraFootage
        carriage_id, camera_id = 5, 13
        codec = 'codec'

        dir_path = os.path.dirname(os.path.realpath(__file__))
        img_file = dir_path + '/' + img_file

        # Test the 3 different ways to create a frame
        frame_3 = Frame(camera_id, codec, img_file)
        frame_2 = Frame(camera_id, codec, frame_3.image)
        test_camera_footage = CameraFootage(carriage_id, [frame_2])
        test_camera_footage.add_frame(frame_3)

        # Check if the container has all the right data
        self.assertEqual(test_camera_footage.carriage_id, carriage_id)
        self.assertEqual(len(test_camera_footage.frames), 2)

        self.assertEqual(test_camera_footage.frames[0], frame_2)
        self.assertEqual(test_camera_footage.frames[1], frame_3)
        self.assertEqual(test_camera_footage.frames[0], test_camera_footage.frames[1])

        self.assertIsNotNone(test_camera_footage.timestamp)

    def test_create_config_update_container(self):
        carriage_id = 5
        test_type = "test_type"
        model_update = {"test": "test"}
        test_model_update = ConfigUpdate(carriage_id, test_type, model_update)

        # Check if the container has all the right data
        self.assertEqual(test_model_update.carriage_id, carriage_id)
        self.assertEqual(test_model_update.data, model_update)
        self.assertIsNotNone(test_model_update.timestamp)

    def test_create_carriage_data_container(self):
        carriage_id, carriage_size, carriage_type = 5, 80, 1
        test_carriage_data = CarriageData(carriage_id, carriage_size, carriage_type)

        # Check if the container has all the right data
        self.assertEqual(test_carriage_data.carriage_id, carriage_id)
        self.assertEqual(test_carriage_data.size, carriage_size)
        self.assertEqual(test_carriage_data.type, carriage_type)
        self.assertIsNotNone(test_carriage_data.timestamp)

    def test_marshal_unmarshal_occupancy_container(self):
        carriage_id = 5
        seat_map = {'1': True, '2': False, '3': True, '4': False}
        free_seats, fill_rate = 2, 0.5
        test_occupancy = OccupancyData(carriage_id, seat_map, free_seats, fill_rate)

        # Transform object to json so it can be sent over the network
        json = test_occupancy.marshal()

        # Transform the json back to the original object
        test_occupancy_2 = DataContainer.unmarshal(json)

        # Transform object to json so it can be sent over the network
        json = test_occupancy_2.marshal()

        # Transform the json back to the original object
        test_occupancy_3 = DataContainer.unmarshal(json)

        self.assertEqual(test_occupancy, test_occupancy_3)

    def test_marshal_unmarshal_camera_footage_container(self, file='./test/testfiles/images/SampleImage.png'):
        carriage_id, camera_id = 5, 13
        codec = 'codec'

        image_bytes = cv2.imread(file)

        frame = Frame(camera_id, codec, image_bytes)
        test_camera_footage = CameraFootage(carriage_id, [frame])

        # Transform object to json so it can be sent over the network
        json = test_camera_footage.marshal()

        # Transform the json back to the original object
        test_camera_footage_2 = DataContainer.unmarshal(json)

        # Transform object to json so it can be sent over the network
        json = test_camera_footage_2.marshal()

        # Transform the json back to the original object
        test_camera_footage_3 = DataContainer.unmarshal(json)

        self.assertEqual(test_camera_footage, test_camera_footage_3)

    def test_marshal_unmarshal_model_update_container(self):
        carriage_id = 5
        config_type = "test_type"
        model_update = {"test": "test"}
        test_model_update = ConfigUpdate(carriage_id, config_type, model_update)

        # Transform object to json so it can be sent over the network
        json = test_model_update.marshal()

        # Transform the json back to the original object
        test_model_update_2 = DataContainer.unmarshal(json)

        # Transform object to json so it can be sent over the network
        json = test_model_update_2.marshal()

        # Transform the json back to the original object
        test_model_update_3 = DataContainer.unmarshal(json)

        test_model_update_3.timestamp = 0
        test_model_update.timestamp = 0
        self.assertEqual(test_model_update, test_model_update_3)

    def test_marshal_unmarshal_carriage_data_container(self):
        carriage_id, carriage_size, carriage_type = 5, 80, 1
        test_carriage_data = CarriageData(carriage_id, carriage_size, carriage_type)

        # Transform object to json so it can be sent over the network

        json = test_carriage_data.marshal()

        # Transform the json back to the original object
        test_carriage_data_2 = DataContainer.unmarshal(json)

        # Transform object to json so it can be sent over the network
        json = test_carriage_data_2.marshal()

        # Transform the json back to the original object
        test_carriage_data_3 = DataContainer.unmarshal(json)

        self.assertEqual(test_carriage_data, test_carriage_data_3)
