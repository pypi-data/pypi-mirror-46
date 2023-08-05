from collections import defaultdict

from src.logger import Logger
from src.singleton import Singleton


class Broker(metaclass=Singleton):
    """
    Broker component for pub sub system. Listeners subscribe to the broker for certain message types.
    When a certain message is published. The broker warns all the listeners that are subscribed to this message type.
    The metaclass of this class is Singleton, which allows us to call Broker(), which will always return the
    existing Broker instance or, if it doesn't exist yet, create a new one.
    """

    def __init__(self):
        """Initialization of the broker, an empty map for the message types and their listeners is created."""
        self.subscription_map = defaultdict()
        self.logger = Logger()

    def subscribe(self, listener, *args):
        """Subscribe a listener for a certain message_type.

        arguments:
        listener -- The listener that wants to subscribe to the broker
        *args -- The message types, the listener wants to subscribe to.
        """
        for message_type in args:
            if message_type not in self.subscription_map:
                self.subscription_map[message_type] = [listener]
            else:
                self.subscription_map[message_type].append(listener)
            self.logger.debug(f'Added callback for message type "{message_type}" from listener "{listener}"',
                              location=self.__class__.__name__)

    def unsubscribe(self, listener, *args):
        """Unsubscribe a listener for a certain message_type."""
        for message_type in args:
            self.subscription_map[message_type].remove(listener)
            if len(self.subscription_map[message_type]) == 0:
                self.subscription_map.pop(message_type)

    def clear_listeners(self):
        """Clear the subscription_map and thus unsubscribe all listeners"""
        self.subscription_map = defaultdict()

    def publish(self, event):
        """
        publish a message of a certain message_type to all of it's listeners.

        arguments:
        message_type -- The message type of the message to be published
        message -- The message to be published
        """
        if event.type in self.subscription_map:
            for listener in self.subscription_map[event.type]:
                listener.get_callback_map()[event.type](event.message)
                self.logger.debug(
                    f'Sent message of type "{event.type}" to "{listener}".',
                    location=self.__class__.__name__
                )

    def has_listener(self, listener):
        return listener in self.subscription_map



class EventListener:
    """
    Abstract Listeners class. Every listeners should implement this class.
    """

    _class_callback_map = {}

    def __init__(self):
        self._callback_map = defaultdict(list, self._class_callback_map.copy())

    def get_callback_map(self):
        return self._callback_map

    def set_message_type_callback(self, message_type, callback):
        """Set a callback for a certain message_type

        message_type -- message_type
        callback -- callback function
        """
        self._callback_map[message_type] = callback

    def __str__(self):
        return self.__class__.__name__


class Event:
    def __init__(self, message_type, message):
        self.type = message_type
        self.message = message
