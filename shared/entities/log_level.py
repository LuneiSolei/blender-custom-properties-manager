import logging

from enum import Enum

class LogLevel(Enum):
    NONE = int(logging.CRITICAL + 1)
    DEBUG = int(logging.DEBUG)
    INFO = int(logging.INFO)
    WARNING = int(logging.WARNING)
    ERROR = int(logging.ERROR)
    CRITICAL = int(logging.CRITICAL)