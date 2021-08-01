import logging
from pythonjsonlogger import jsonlogger


def get_logger():
    logger = logging.getLogger("cloud-ca")
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(jsonlogger.JsonFormatter())

    logger.addHandler(stdout_handler)
    return logger
