import logging
import logging.handlers
import os
import sys
from logging import Logger

from rich.logging import RichHandler

RICH_FORMAT = "| %(filename)s:%(lineno)s\t| %(message)s"
FILE_HANDLER_FORMAT = "[%(asctime)s]\t%(levelname)s\t[%(filename)s:%(lineno)s]\t>> %(message)s"


def set_logger(path: str, name: str) -> Logger:
    logging.basicConfig(level="NOTSET", format=RICH_FORMAT, handlers=[RichHandler(rich_tracback=True)])
    file_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(path, name), when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    file_handler.suffix = "logs=%Y%m%d"
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(FILE_HANDLER_FORMAT))

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
