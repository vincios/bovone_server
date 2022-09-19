import logging
import os

from ..dependencies import get_settings

config = get_settings()

LOGFILE = os.path.abspath("log.log")
FILE_HANDLER, CONSOLE_HANDLER = logging.FileHandler(LOGFILE, "a+"), logging.StreamHandler()

CONFIG_LOGGING_LEVEL = "DEBUG" if config.debug else "INFO"
DEFAULT_LOGGING_LEVEL = logging.getLevelName(CONFIG_LOGGING_LEVEL)


def get_logger(name, level=None, console=True):
    formats = {"console": '[%(levelname)5s] [%(filename)s:%(lineno)s %(funcName)s()]: \u001b[37m %(message)s\033[0m',
               "file": '[%(levelname)5s] [%(process)5d: %(filename)s:%(lineno)s %(funcName)s()]: %(message)s'}

    logger = logging.getLogger(name)
    level = level if level else DEFAULT_LOGGING_LEVEL
    logger.setLevel(level)

    if console:
        CONSOLE_HANDLER.setFormatter(logging.Formatter(formats["console"]))
        CONSOLE_HANDLER.setLevel(level)
        logger.addHandler(CONSOLE_HANDLER)

    FILE_HANDLER.setFormatter(logging.Formatter(formats["file"]))
    FILE_HANDLER.setLevel(level)

    logger.addHandler(FILE_HANDLER)

    return logger
