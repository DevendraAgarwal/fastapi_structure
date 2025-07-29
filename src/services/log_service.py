"""Class For Handling Logs
"""

import os
import logging
from threading import Lock
from typing import Optional, Dict

from fastapi import Request

from src.services.environment_service import env
from src.services.log_formatter.gcp_json_formatter import GCPJsonFormatter


class LogService:
    """
    Singleton Custom Logger for FastAPI that outputs structured JSON logs.
    Supports logging to both stdout and a local file.
    """

    _initialized = False
    _instance = None
    _lock = Lock()

    def __new__(
            cls,
            name: str = env.get("APP_NAME"),
            level: str = "INFO",
            log_file: Optional[str] = None
            ):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LogService, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(
            self,
            name: str = env.get("APP_NAME"),
            level: str = "INFO",
            log_file: Optional[str] = env.get("LOG_FILE")
            ):
        """
        Initialize logger if not already initialized.
        Args:
            name (str): Logger name.
            level (str): Logging level (e.g., DEBUG, INFO).
            log_file (str): Optional file path to write logs.
        """
        if self._initialized:
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level.upper())
        self._setup_handler(log_file)
        self._initialized = True

    def _setup_handler(self, log_file: Optional[str]):
        """
        Configures the logger to output to both stdout
        and optionally to a file.
        Args:
            log_file (str): Path to local log file.
        """
        if not self.logger.handlers:
            formatter = GCPJsonFormatter(
                '%(asctime)s %(levelname)s %(message)s'
                )

            # Stream Handler (for stdout)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

            # File Handler (for local file logging)
            if log_file:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.
        Returns:
            logging.Logger
        """
        return self.logger

    def log_request(
            self,
            request: Request,
            message: str,
            level: str = "INFO",
            extra: Optional[Dict] = None
            ):
        """
        Logs a FastAPI request with relevant metadata.
        Args:
            request (Request): FastAPI request object.
            message (str): Message to log.
            level (str): Logging level.
            extra (dict): Additional fields to include.
        """
        log_data = {
            "client_ip": request.client.host,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "message": message
        }
        if extra:
            log_data.update(extra)

        self._log(level, log_data)

    def _log(self, level: str, data: dict):
        """
        Internal helper to log data at a specified level.
        Args:
            level (str): Logging level.
            data (dict): Structured log data.
        """
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func("", extra={"props": data})


logger = LogService(level="DEBUG").get_logger()
