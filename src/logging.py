"""
Logging configuration module.

This module provides functionality to configure logging for the application,
including custom log levels and formatting options. It defines:
- LogLevels: Enumeration of standard logging levels
- configure_logging: Function to set up logging with appropriate level
and format
"""

import logging
from enum import Enum

LOG_FORMAT_DEBUG = """%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:
%(lineno)d"""


class LogLevels(str, Enum):
    """Enumeration of standard logging levels.

    Attributes
    ----------
    debug : str
        Debug level logging.
    info : str
        Info level logging.
    warning : str
        Warning level logging.
    error : str
        Error level logging.
    critical : str
        Critical level logging.
    """

    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


def configure_logging(log_level: str = LogLevels.error):
    """
    Configure the logging settings for the application.

    Args:
        level (str): The logging level to set. Defaults to LogLevels.error.
    """
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    if log_level not in log_levels:
        logging.basicConfig(level=logging.ERROR)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
