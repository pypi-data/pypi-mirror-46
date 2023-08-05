import unittest

from src import EventListener, Broker, Event


class _TestSingleListener(EventListener):
    def __init__(self):
        super().__init__()
        self.fill_listener_map()
        self.test_value = 0

    def fill_listener_map(self):
        self.get_callback_map()['test'] = self.test_callback

    def test_callback(self, message):
        self.test_value = message


class _TestMultipleListener(EventListener):
    _class_callback_map = {}

    def __init__(self):
        super().__init__()
        self.fill_listener_map()
        self.test_value = 0

    def fill_listener_map(self):
        self.get_callback_map()['test'] = self.test_callback
        self.get_callback_map()['test_double'] = self.test_double_callback
        self.get_callback_map()['test_triple'] = self.test_triple_callback

    def test_callback(self, message):
        self.test_value = message

    def test_double_callback(self, message):
        self.test_value = 2 * message

    def test_triple_callback(self, message):
        self.test_value = 3 * message


class BrokerTests(unittest.TestCase):
    def test_pub_sub_single(self):
        broker = Broker()
        listener = _TestSingleListener()

        # Subscribe & Publish
        broker.subscribe(listener, 'test')
        broker.publish(Event('test', 5))

        # Check if any message was received
        self.assertEqual(listener.test_value, 5)

    def test_pub_sub_multiple(self):
        broker = Broker()
        listener = _TestMultipleListener()

        # Subscribe
        broker.subscribe(listener, 'test', 'test_double', 'test_triple')

        # Test if correct callbacks are applied
        broker.publish(Event('test_triple', 5))
        self.assertEqual(listener.test_value, 15)
        broker.publish(Event('test', 5))
        self.assertEqual(listener.test_value, 5)
        broker.publish(Event('test_double', 5))
        self.assertEqual(listener.test_value, 10)

    def test_pub_sub_multiple_listeners(self):
        broker = Broker()
        listener1 = _TestMultipleListener()
        listener2 = _TestSingleListener()
        listener3 = _TestSingleListener()

        # Subscribe & publish
        broker.subscribe(listener1, 'test', 'test_double')
        broker.subscribe(listener2, 'test')
        broker.subscribe(listener3, 'test')
        broker.publish(Event('test', 5))

        # Test if all listeners receive message
        self.assertEqual(listener1.test_value, 5)
        self.assertEqual(listener2.test_value, 5)
        self.assertEqual(listener3.test_value, 5)

        broker.publish(Event('test_double', 5))
        self.assertEqual(listener1.test_value, 10)
        self.assertEqual(listener2.test_value, 5)
        self.assertEqual(listener3.test_value, 5)

    def test_subscribe_unsubscribe(self):
        broker = Broker()
        listener = _TestMultipleListener()

        # Subscribe
        broker.subscribe(listener, 'test', 'test_double', 'test_triple')

        # Test if correct callbacks are applied
        broker.publish(Event('test_triple', 5))
        self.assertEqual(listener.test_value, 15)
        broker.publish(Event('test', 5))
        self.assertEqual(listener.test_value, 5)
        broker.publish(Event('test_double', 5))
        self.assertEqual(listener.test_value, 10)

        broker.unsubscribe(listener, 'test')

        # Publish some messages and check if listener doesn't receive the 'test' message
        broker.publish(Event('test_triple', 5))
        self.assertEqual(listener.test_value, 15)
        broker.publish(Event('test', 5))
        self.assertEqual(listener.test_value, 15)
        broker.publish(Event('test_double', 5))
        self.assertEqual(listener.test_value, 10)

        broker.clear_listeners()

        # Publish some messages and check if listener doesn't receive them
        broker.publish(Event('test_triple', 5))
        self.assertEqual(listener.test_value, 10)
        broker.publish(Event('test', 5))
        self.assertEqual(listener.test_value, 10)
        broker.publish(Event('test_double', 5))
        self.assertEqual(listener.test_value, 10)
