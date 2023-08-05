"""
Logger util module.
This module wraps the logging library of python, but handles the writing of logging files in a more standard way.
There is also only one Logger object as it uses the singleton metaclass. Due to this, the first invocation of a logger
object should set the correct path of the log file.
"""

from src.logger.logger import Logger

__all__ = ["Logger"]
