import logging
from pathlib import Path

from src.configuration_store import ConfigurationStore
from src.singleton import Singleton


class Logger(metaclass=Singleton):
    """
    Logger which logs to the given file path and wraps the logging library methods.
    The logging_levels are the same as the logging library in descending levels:

    CRITICAL
    ERROR
    WARNING
    INFO
    DEBUG
    NOTSET

    All levels above the given level will be logged.
    For example if one chooses 'DEBUG' as a log level in the config,
    DEBUG, INFO, WARNING, ERROR & CRITICAL will be logged.
    """

    def __init__(self, file_path=None):
        self._logging_level = None

        current_exec_path = Path().absolute()
        self.file_path = f'{current_exec_path}/{file_path}' if file_path is not None \
            else f'{current_exec_path}/{ConfigurationStore().get_value("logging_path")}'
        if 'logging_level' in ConfigurationStore():
            self._logging_level = ConfigurationStore().get_value('logging_level')
            logging.basicConfig(level=getattr(logging, self._logging_level), filename=self.file_path, filemode='w+',
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                datefmt='%d-%m-%y %H:%M:%S')

    def log(self, log_level, message, *args, location='', **kwargs):
        if self._logging_level is not None:
            prefix = f'[{location}]:' if location is not '' else ''
            return logging.log(log_level, f'{prefix} {message}', *args, **kwargs)
        else:
            pass

    def debug(self, *arg, **kwargs):
        self.log(logging.DEBUG, *arg, **kwargs)

    def info(self, *arg, **kwargs):
        self.log(logging.INFO, *arg, **kwargs)

    def warning(self, *arg, **kwargs):
        self.log(logging.WARNING, *arg, **kwargs)

    def error(self, *arg, **kwargs):
        self.log(logging.ERROR, *arg, **kwargs)
