from src.configuration_store.configuration_store import ConfigurationStore


class ConfigurationLoader:
    """Class that handles the loading and decoding of configuration files"""

    def __init__(self, configuration_decoder, configuration_store=ConfigurationStore()):
        self.loaded_files = set()
        self.configuration_store = configuration_store
        self._configuration_decoder = configuration_decoder

    def load_config(self, filename):
        """Load the config file, decode it and add the file to the loaded files"""

        if filename in self.loaded_files:
            return
        else:
            self.loaded_files.add(filename)
            for key, value in self._configuration_decoder.decode_config(filename):
                self._set_value(key, value)

    def _set_value(self, key, value):
        """Set the value in the configuration_store"""

        self.configuration_store.set_value(key, value)


class StaticConfigurationLoader(ConfigurationLoader):
    """A configuration loader which uses the standard static ConfigurationStore"""

    def __init__(self, configuration_decoder):
        super().__init__(configuration_decoder)
