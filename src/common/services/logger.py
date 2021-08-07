import logging

from pythonjsonlogger import jsonlogger


def get_logger():
    """ Function to set up and return a logger instance.

    Returns
    -------
    A python logging instance that can be used throughout the application.
    """
    logger = logging.getLogger("cloud-ca")
    logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(jsonlogger.JsonFormatter())

    logger.addHandler(stdout_handler)
    return logger
