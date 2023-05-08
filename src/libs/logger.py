import logging
from logging import config

from .settings import AppSettings

settings = AppSettings()

__all__ = ['setup_logger']


class LevelOnlyFilter:
    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


LOGGING_CONFIG = {
        "version": 1,
        "loggers": {
                "": {
                        "level": "DEBUG",
                        "propagate": False,
                        "handlers": ["stream_handler", "file_handler"],
                        },
                # "root": {
                #         "level": "DEBUG",
                #         "propagate": False,
                #         "handlers": ["stream_handler", "file_handler"],
                #         },
                # "asyncio": {
                #         "level": "WARNING",
                #         "propagate": False,
                #         "handlers": ["stream_handler"],
                #         },
                "PIL": {
                        "level": "INFO",
                        "propagate": False,
                        "handlers": ["stream_handler"],
                        },
                "HANDLERS_BASICS": {
                        "level": "DEBUG",
                        "propagate": False,
                        "handlers": ["stream_handler", "file_handler"],
                        },
                "telegram": {
                        "level": "WARNING",
                        "propagate": False,
                        "handlers": ["stream_handler", "file_handler"],
                        },
                "apscheduler": {
                        "level": "INFO",
                        "propagate": False,
                        "handlers": ["stream_handler"],
                        },

                settings.DEFAULT_NAME: {
                        "level": "DEBUG",
                        "propagate": False,
                        "handlers": ["stream_handler", "file_handler"],
                        },
                },
        "handlers": {
                "stream_handler": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                        "level": "DEBUG",
                        # "filters": ["only_warning"],
                        "formatter": "default_formatter",
                        },
                "file_handler": {
                        "class": "logging.FileHandler",
                        "filename": settings.LOG_FILE,
                        "mode": "a",
                        "level": "DEBUG",
                        "formatter": "file_formatter",
                        },
                },
        "filters": {
                "only_warning": {
                        "()": LevelOnlyFilter,
                        "level": logging.WARN,
                        },
                },
        "formatters": {
                "default_formatter": {
                        "format": "%(levelname)s: %(name)s - %(message)s",
                        },
                "file_formatter": {
                        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        },
                },
        }


def setup_logger(name: str):
    """Setup a logger using defaults

    Reference:
    https://towardsdatascience.com/basic-to-advanced-logging-with-python-in-10-minutes-631501339650
    https://www.mybluelinux.com/python-logging-config-via-dictionary-and-config-file/
    """

    config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)

    return logger
