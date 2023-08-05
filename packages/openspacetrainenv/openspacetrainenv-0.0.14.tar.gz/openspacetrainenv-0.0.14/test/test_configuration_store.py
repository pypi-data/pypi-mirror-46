import os
import unittest

from src import ConfigurationStore, JsonConfigurationDecoder, ConfigurationLoader

dirname = os.path.dirname(__file__)


class TestConfigurationStore(unittest.TestCase):
    def test_store(self):
        configuration_store = ConfigurationStore()

        # Fill in the values
        for i in range(0, 100):
            configuration_store.set_value(i, i)

        # Check the values
        for i in range(0, 100):
            self.assertEqual(configuration_store.get_value(i), i)

    def test_singleton_store(self):
        configuration_store_1 = ConfigurationStore()
        configuration_store_2 = ConfigurationStore()

        # Check if both stores are equal and no new store has been created.
        self.assertEqual(configuration_store_1, configuration_store_2)

    def test_types(self):
        configuration_store = ConfigurationStore()
        types = [set, dict, list, int, float, str]

        # Fill in the values
        for i, value in enumerate(types):
            configuration_store.set_value(i, value())

        # Check the values
        for i, value in enumerate(types):
            self.assertEqual(configuration_store.get_value(i), value())


class TestJsonConfigurationDecoder(unittest.TestCase):
    def test_config_decoder(self):
        decoded = JsonConfigurationDecoder().decode_config(f'{dirname}/../test/testfiles/json/test.json')

        # Map from json
        result_map = {k: v for k, v in decoded}

        # Map we should get
        default_map = {"a": 1, "b": 2, "c": 3}

        # Check if both are the same
        self.assertEqual(result_map, default_map)


class TestJsonConfigurationLoader(unittest.TestCase):
    def test_static_config_loader(self):
        json_file = f'{dirname}/../test/testfiles/json/test.json'

        # We use our own created ConfigurationStore to not share the same store across tests
        config_loader = ConfigurationLoader(JsonConfigurationDecoder())

        # Load the config
        config_loader.load_config(json_file)

        # Check if the loaded files contain the last loaded file
        self.assertTrue(json_file in config_loader.loaded_files)

        # Map we should get
        default_map = {"a": 1, "b": 2, "c": 3}

        # Check if the values are present in the configuration store and if they are equal
        for k, v in default_map.items():
            self.assertEqual(config_loader.configuration_store.get_value(k), v)
