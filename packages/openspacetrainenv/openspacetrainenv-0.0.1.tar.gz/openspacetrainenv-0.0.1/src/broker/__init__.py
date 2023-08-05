"""This module contains the broker class, used to send events around the train environment. The broker uses a Pub-Sub architecture.
All communication passes through this broker, which is a singleton, so only one is present on the entire environment.
Plugins should override the Event class so that they can publish these events to other components that implement the EventListener interface.
"""

from src.broker.broker import Broker, EventListener, Event

__all__ = ['Broker', 'EventListener', 'Event']
