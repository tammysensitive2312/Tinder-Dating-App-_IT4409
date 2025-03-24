import logging
import logging.handlers

class PyLogger:
    _instance = None

    def __new__(cls, log_file='truong.log', max_bytes=2 * 1024 * 1024, backup_count=5):
        if cls._instance is None:
            cls._instance = super(PyLogger, cls).__new__(cls)
            cls._instance._setup_logger(log_file, max_bytes, backup_count)
        return cls._instance

    def _setup_logger(self, log_file, max_bytes, backup_count):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            # Rotate file handler
            rotate_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            rotate_handler.setLevel(logging.DEBUG)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Formatters
            rotate_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

            # Set formatters
            rotate_handler.setFormatter(rotate_formatter)
            console_handler.setFormatter(console_formatter)

            # Add handlers to the logger
            self.logger.addHandler(rotate_handler)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def debug(self, message):
        self.logger.debug(message)