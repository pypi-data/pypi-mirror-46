from src.singleton import Singleton


class ConfigurationStore(metaclass=Singleton):
    """Singleton class of a store of configuration values"""

    def __init__(self):
        self._configuration_values = {}

    def get_value(self, name):
        return self._configuration_values[name]

    def set_value(self, name, value):
        self._configuration_values[name] = value

    def __contains__(self, item):
        return self._configuration_values.__contains__(item)
