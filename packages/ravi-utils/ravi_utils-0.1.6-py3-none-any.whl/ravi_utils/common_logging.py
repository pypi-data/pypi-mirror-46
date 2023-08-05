# -*- coding: utf-8 -*-
"""Common log functions"""

import logging

from .common_files import FileOps


class LogOps:

    """Log operations"""

    MAX_BYTES = 10 * 1024 * 1024

    @staticmethod
    def setup_logging(log_dir_path, log_file_name, log_level, max_bytes=MAX_BYTES, file_count=10):
        """Set up logging"""
        log_formatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        logger = logging.getLogger()
        logger.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

        # File handler
        FileOps.create_dir_if_not_exists(log_dir_path)
        file_handler = logging.handlers.RotatingFileHandler(
            "{0}/{1}.log".format(log_dir_path, log_file_name),
            maxBytes=max_bytes, backupCount=file_count)

        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)
