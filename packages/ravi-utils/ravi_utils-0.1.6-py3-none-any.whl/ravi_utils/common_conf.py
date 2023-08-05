# -*- coding: utf-8 -*-
"""Common conf functions"""

import json
import logging
import logging.handlers
import pathlib
import sys


class ConfOps:

    """Conf operations"""

    @staticmethod
    def load_conf(path_str, encoding="utf8"):
        """Returns configuration from file as json"""
        conf_file_path = pathlib.Path(path_str)
        if not conf_file_path.exists or not conf_file_path.is_file():
            logging.info("Conf file %s not found! Exiting...", path_str)
            sys.exit(1)
        elif conf_file_path.stat().st_size == 0:
            logging.info("Conf file %s is empty! Exiting...", path_str)
            sys.exit(1)

        try:
            with open(path_str, mode="r", encoding=encoding) as file_handle:
                return json.load(file_handle)
        except IOError as io_err:
            logging.info("I/O error(%s): %s", io_err.errno, io_err.strerror)

    @staticmethod
    def check_conf(conf_json, key_list):
        """Checks if conf has all necessary keys, exiting otherwise"""
        for key in key_list:
            if key not in conf_json or len(str(conf_json[key])) is 0:
                logging.info("No %s in config! Exiting ... ", key)
                sys.exit(1)

        return conf_json

    @staticmethod
    def init_conf(conf_file_path, req_conf_key_list):
        """
        Init conf, conf file path and required key list as parameters
        Returns conf dictionary
        """
        conf_json = ConfOps.load_conf(conf_file_path)
        conf_dict = ConfOps.check_conf(conf_json, req_conf_key_list)

        return conf_dict
