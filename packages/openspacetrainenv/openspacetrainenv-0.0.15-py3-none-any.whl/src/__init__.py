import importlib
import os
import traceback
from pathlib import Path

from src.broker import Broker, EventListener, Event
from src.configuration_store import ConfigurationStore, ConfigurationLoader, JsonConfigurationDecoder, \
    ConfigurationDecoder
from src.data_container import DataContainer, OccupancyData, DataTypes
from src.logger import Logger
from src.main import main
from src.singleton import Singleton

name = "openspacetrainenv"

__all__ = ["Broker", "ConfigurationStore", "ConfigurationLoader", "ConfigurationDecoder", "JsonConfigurationDecoder",
           "EventListener", "Event", "DataTypes", "DataContainer", "OccupancyData", "Singleton", "Logger"]

dir_path = os.path.dirname(os.path.realpath(__file__))
current_exec_path = Path().absolute()

store = ConfigurationStore()
loader = ConfigurationLoader(JsonConfigurationDecoder(), store)
loader.load_config(f'{current_exec_path}/main_config.json')

try:
    exec(
        compile(open(f'{current_exec_path}/settings.py', "rb").read(), f'{current_exec_path}/settings.py', 'exec'),
        globals(),
        locals()
    )
    for k, v in globals()['KWARGS'].items():
        store.set_value(k, v)

except Exception as e:
    traceback.print_tb(e.__traceback__)


def init_as_main():
    load_plugins_from_path(current_exec_path.joinpath('plugin'))
    for plugin in globals()['PLUGINS']:
        load_plugins_from_pip(plugin)
    main()


def load_plugins_from_pip(package):
    pkg = None
    if package not in globals():
        try:
            pkg = importlib.import_module(package)
        except ImportError:
            print(f'Invalid package: The package with name "{package}" was not installed on the system. Please make '
                  f'sure it is installed, either using pip or present in the plugin folder.')
        finally:
            globals()[package] = pkg
    else:
        print(f'Using the plugin from the plugin folder instead of its pip package. {package}')


def load_plugins_from_path(path, check_globals=False):
    import sys
    tree = os.listdir(path)

    sys.path.insert(0, path)
    for plugin in tree:
        if not check_globals or plugin not in globals():
            load_plugin(os.path.join(path, plugin), plugin)
        else:
            print(f'Already imported plugin with name: {plugin}')


def load_plugin(path, plugin_name):
    if os.path.isdir(path):
        plugin_obj = importlib.import_module('plugin.{}'.format(plugin_name))
        globals()[plugin_name] = plugin_obj


if __name__ == '__main__':
    init_as_main()
