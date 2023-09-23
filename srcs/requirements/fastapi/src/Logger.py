import logging
from logging.handlers import RotatingFileHandler
import os

from dataclasses import dataclass

log_path = os.environ["PATH_LOG"]

@dataclass
class Logger:

    def set_logger(self, path: str) -> None:

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        stream_log = logging.StreamHandler()
        stream_log.setLevel(logging.DEBUG)
        stream_log.setFormatter(formatter)

        self.logger.addHandler(stream_log)

        file_log = RotatingFileHandler(path, maxBytes=5 * 1024 * 1024)
        self.logger.addHandler(file_log)

        self.logger.info("LOGGER CONFIGURED")

logger = Logger()
logger.set_logger(log_path)
