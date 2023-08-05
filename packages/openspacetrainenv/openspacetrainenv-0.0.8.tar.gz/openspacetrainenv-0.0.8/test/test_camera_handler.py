import math
import os
import unittest
from time import sleep

import cv2
import numpy

from plugin.camera_handler import CameraHandler, CodecListener, IntervalCameraHandler, Transcoder, \
    ImageCameraHandler, VideoCameraHandler, MultiVideoCameraHandler, MultiVideoTranscoder, CameraFootage, StreamHandler, \
    Frame
from src import Broker
from src import DataTypes

dirname = os.path.dirname(__file__)


class TestCodecListener(CodecListener):
    __test__ = False

    def on_publish(self, footage):
        self.received_footage += [footage]

    def __init__(self, codec):
        super().__init__(self.on_publish, codec)
        self.received_footage = []


class TestIntervalCameraHandler(IntervalCameraHandler):
    __test__ = False

    def __init__(self, delay, codec):
        super().__init__(delay)
        self.codec = codec

    def _retrieve_footage(self):
        return TestFootage(self.codec)


class TestFootage(CameraFootage):
    __test__ = False

    def __init__(self, codec):
        super().__init__(None, [Frame(None, codec, f'{dirname}/../test/testfiles/images/SampleImage.png')])


class CameraHandlerTests(unittest.TestCase):
    def setUp(self):
        DataTypes().add_datatype(TestFootage)

    def test_pub_sub_simple(self):
        codec = 'codec'
        broker = Broker()
        cam_handler = CameraHandler(0)
        listener = TestCodecListener(codec)
        transcoder = Transcoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')

        # Subscribe & Publish
        broker.subscribe(listener, codec)
        cam_handler.publish(TestFootage(codec))

        # Check if any footage was received
        self.assertTrue(listener.received_footage is not None)

    def test_pub_sub_multiple(self):
        broker = Broker()
        codec = 'codec'
        cam_handler = CameraHandler(0)
        transcoder = Transcoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')
        listeners = [TestCodecListener(codec) for i in range(0, 10)]

        # Subscribe all the listeners & Publish
        for listener in listeners:
            broker.subscribe(listener, codec)
        cam_handler.publish(TestFootage(codec))

        # Check if all listeners received the footage
        for listener in listeners:
            self.assertEqual(len(listener.received_footage), 1)

    @staticmethod
    def simple_transform(footage):
        footage.codec = 'y'
        return footage

    def test_transform(self):
        broker = Broker()
        codec = 'y'
        cam_handler = CameraHandler(0)
        transcoder = Transcoder(codec, self.simple_transform)
        transcoder.add_footage_source('camera_handler')
        listener = TestCodecListener(codec)

        # Subscribe & Publish
        broker.subscribe(listener, codec)
        cam_handler.publish(TestFootage('x'))

        # Check if any footage was received
        self.assertEqual(len(listener.received_footage), 1)

        # Check if the transform has been applied successfully
        self.assertEqual(listener.received_footage[0].codec, 'y')


class ImageCameraHandlerTests(unittest.TestCase):
    def setUp(self):
        DataTypes().add_datatype(TestFootage)

    def image_publish(self, delay=1, handler_delay=0.5, img_file='../test/testfiles/images/SampleImage.png'):
        # Create an Image Camera Handler with a random object
        broker = Broker()
        broker.clear_listeners()
        codec = 'numpy'
        transcoder = Transcoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')
        handler = ImageCameraHandler(handler_delay, f'{dirname}/{img_file}', 0)
        listener = TestCodecListener(codec)
        broker.subscribe(listener, codec)

        # Start the handler
        handler.start()
        self.assertNotEqual(handler.thread, None)

        # Sleep for a given delay
        sleep(delay)

        # Stop the handler
        handler.stop()
        self.assertEqual(handler.thread, None)

        # Check if we received enough footage objects
        self.assertAlmostEqual(len(listener.received_footage), math.floor(delay / handler_delay), delta=1)

        # Check if the retrieved frame equals the frame we sent to the CameraHandler
        self.assertTrue(
            numpy.array_equal(cv2.imread(f'{dirname}/{img_file}'), listener.received_footage[0].frames[0].image))

    def test_all_image_formats(self):
        formats = ['jpg', 'png']
        for codec in formats:
            self.image_publish(img_file=f'../test/testfiles/images/SampleImage.' + codec)


class StreamHandlerTests(unittest.TestCase):
    def frame_publish(self, delay=1, handler_delay=0.5, video_file='../test/testfiles/videos/SampleVideo.mp4'):
        broker = Broker()
        broker.clear_listeners()
        codec = 'numpy'
        # Create an Image Camera Handler with a random object
        handler = StreamHandler(handler_delay, f'{dirname}/{video_file}', 0)
        listener = TestCodecListener(codec)
        transcoder = Transcoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')
        broker.subscribe(listener, codec)

        # Start the handler
        handler.start()
        self.assertNotEqual(handler.thread, None)

        # Sleep for a given delay
        sleep(delay)

        # Stop the handler
        handler.stop()
        self.assertEqual(handler.thread, None)

        # Check if we received enough footage objects, higher delta, because of the opening and closing of VideoCapture
        self.assertAlmostEqual(len(listener.received_footage), math.floor(delay / handler_delay), delta=2)

    def test_all_video_formats(self):
        formats = ['flv', 'mkv', 'mp4']
        for codec in formats:
            self.frame_publish(video_file=f'../test/testfiles/videos/SampleVideo.' + codec)


class VideoCameraHandlerTests(unittest.TestCase):
    def setUp(self):
        DataTypes().add_datatype(TestFootage)

    def video_publish(self, delay=1, handler_delay=0.5, video_file='../test/testfiles/videos/SampleVideo.mp4'):
        self.skipTest(
            "This test was created before the introduction of config files and streamhandler is not relevant anymore")
        broker = Broker()
        broker.clear_listeners()
        codec = 'numpy'
        # Create an Image Camera Handler with a random object
        handler = VideoCameraHandler(handler_delay, f'{dirname}/{video_file}', 0)
        listener = TestCodecListener(codec)
        transcoder = Transcoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')
        broker.subscribe(listener, codec)

        # Start the handler
        handler.start()
        self.assertNotEqual(handler.thread, None)

        # Sleep for a given delay
        sleep(delay)

        # Stop the handler
        handler.stop()
        self.assertEqual(handler.thread, None)

        # Check if we received enough footage objects
        self.assertAlmostEqual(len(listener.received_footage), math.floor(delay / handler_delay), delta=1)

        # Check if the retrieved frame equals the frame we sent to the CameraHandler
        video_capture = cv2.VideoCapture(f'{dirname}/{video_file}')
        for footage_object in listener.received_footage:
            success, capture = video_capture.read()

            self.assertTrue(numpy.array_equal(capture, footage_object.frames[0].image))

    def test_all_video_formats(self):
        formats = ['flv', 'mkv', 'mp4']
        for codec in formats:
            self.video_publish(video_file=f'../test/testfiles/videos/SampleVideo.{codec}')

    def test_multi_video_publish(self, delay=4, handler_delay=2):
        self.skipTest(
            "This test was created before the introduction of config files and stream handler is not relevant anymore")
        broker = Broker()
        broker.clear_listeners()
        codec = 'numpy'
        file_map = {
            'mp4': f'{dirname}/../test/testfiles/videos/SampleVideo.mp4',
            'flv': f'{dirname}/../test/testfiles/videos/SampleVideo.flv',
            'mkv': f'{dirname}/../test/testfiles/videos/SampleVideo.mkv'
        }

        handler = MultiVideoCameraHandler(handler_delay, file_map, 0)
        listener = TestCodecListener(codec)
        transcoder = MultiVideoTranscoder(codec, lambda x: x)
        transcoder.add_footage_source('camera_handler')
        broker.subscribe(listener, codec)

        # Start the handler
        handler.start()
        self.assertNotEqual(handler.thread, None)

        # Sleep for a given delay
        sleep(delay)

        # Stop the handler
        handler.stop()
        self.assertEqual(handler.thread, None)

        # Check if we received enough footage objects
        self.assertAlmostEqual(len(listener.received_footage), math.floor(delay / handler_delay), delta=1)

        video_capture_map = {key: cv2.VideoCapture(value) for key, value in file_map.items()}

        # Check if the retrieved frame equals the frame we sent to the CameraHandler
        for footage_object in listener.received_footage:
            for key, value in file_map.items():
                success, capture = video_capture_map[key].read()
                self.assertTrue(numpy.array_equal(capture, footage_object[key].frames[0].image))
