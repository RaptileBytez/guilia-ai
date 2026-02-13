import logging
import os

class Logger:
    """A simple wrapper around Python's built-in logging module.

    This class provides a convenient interface for logging messages to both 
    the console and a file, with configurable log levels and formatting.

    Attributes:
        logger (logging.Logger): The underlying logger instance.
    """
    def __init__(self, name="GenAI", log_file="data/logs/app.log", level=logging.INFO):
        """Initializes the logger with a specified name, log file, and level.

        Args:
            name (str): The name of the logger. Defaults to "GenAI".
            log_file (str): The path to the log file. Defaults to "logs/app.log".
            level: The logging level (e.g., logging.INFO). Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.hasHandlers():
            # Ensure the log directory exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            # Create file handler which logs messages to a file
            fh = logging.FileHandler(log_file)
            fh.setLevel(level)

            # Create console handler with the same log level
            ch = logging.StreamHandler()
            ch.setLevel(level)

            # Create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # Add the handlers to the logger
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

            self.logger.propagate = False  # Prevent log messages from being propagated to the root logger
            self.logger.info("Logger initialized successfully.")

    def info(self, message):
        """Logs an informational message."""
        self.logger.info(message)

    def warning(self, message):
        """Logs a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Logs an error message."""
        self.logger.error(message)

    def debug(self, message):
        """Logs a debug message."""
        self.logger.debug(message)