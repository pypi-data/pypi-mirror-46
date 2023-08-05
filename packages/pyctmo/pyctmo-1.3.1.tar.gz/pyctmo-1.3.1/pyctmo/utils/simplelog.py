import logging
from pathlib import Path
import os

class SimpleLog:

    LOGGER_PATH: str = os.path.join(Path.home(),"Desktop/pyctmo.log")
    LOGGER_NAME: str = "pyctmo"

    def __init__(self, logger_name: str = LOGGER_NAME, logger_path: str = LOGGER_PATH):

        self._logger_name = logger_name
        self._logger_path = logger_path

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        # logger.propagate = False

        if not logger.hasHandlers():

            # File of logs
            logfile = logging.FileHandler(self._logger_path)
            logfile.setLevel(logging.DEBUG)

            # Console Handler : shows everything, except DEBUG
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)

            # Formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
            )
            logfile.setFormatter(formatter)
            console.setFormatter(formatter)

            # Add handlers
            logger.addHandler(logfile)
            logger.addHandler(console)

        self._logger = logger

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)
