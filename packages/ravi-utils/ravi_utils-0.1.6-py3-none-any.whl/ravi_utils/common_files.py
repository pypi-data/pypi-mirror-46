# -*- coding: utf-8 -*-
"""Common file functions"""

import logging
import os
import pathlib


class FileOps:

    """Log operations"""

    @staticmethod
    def get_file_content(path_str, encoding="utf8"):
        """Return file content as string"""
        try:
            with open(path_str, mode="r", encoding=encoding) as file_handle:
                file_content = file_handle.read()
                return file_content
            if not file_content:
                logging.info("File %s was empty", )
                return ""
        except IOError as io_err:
            logging.info("I/O error while reading %s code:%s, error: %s",
                         path_str, io_err.errno, io_err.strerror)

    @staticmethod
    def create_dir_if_not_exists(path_str):
        """Create folder if it does not exists"""
        try:
            if not os.path.exists(path_str):
                os.makedirs(path_str)
        except OSError as os_err:
            logging.info("OS error(%s): %s", os_err.errno, os_err.strerror)

    @staticmethod
    def create_file_if_not_exists(path_str, encoding="utf8"):
        """Create file if it does not exist"""
        file_path = pathlib.Path(path_str)
        # check if file exists
        try:
            if not file_path.exists() or not file_path.is_file():
                # creating empty file
                logging.info("Creating file %s", path_str)
                open(path_str, 'a', encoding=encoding).close()
        except OSError as os_err:
            logging.info("OS error(%s): %s", os_err.errno, os_err.strerror)

    @staticmethod
    def write_file(path_str, content, encoding="utf8"):
        """Write content to file, overwrite existing content"""
        try:
            logging.info("Writing value \"%s\" to file \"%s\"", content, path_str)
            with open(path_str, 'w', encoding=encoding) as file_handle:
                file_handle.write(content)
        except IOError as io_err:
            logging.info("I/O error(%s): %s", io_err.errno, io_err.strerror)
