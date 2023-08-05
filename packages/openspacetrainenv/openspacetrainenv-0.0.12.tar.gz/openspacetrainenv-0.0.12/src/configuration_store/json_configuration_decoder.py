import json

from src.configuration_store.configuration_decoder import ConfigurationDecoder


class JsonConfigurationDecoder(ConfigurationDecoder):
    """Json configuration decoder"""

    def decode_config(self, filename):
        with open(filename) as json_data:
            for key, value in json.load(json_data).items():
                yield key, value
