# -*- coding: utf-8 -*-
"""Common net functions"""

from urllib.error import URLError, HTTPError
from urllib.request import urlopen

import logging


class NetOps:

    """Net operations"""

    @staticmethod
    def get_url_content(url, encoding="utf8"):
        """Returns url content"""
        response = None
        content = ""
        try:
            response = urlopen(url)
            content = response.read().decode(encoding)
        except HTTPError as error:
            logging.info("The server couldn't fulfill the request.")
            logging.info(
                "Error while retrieving %s, code: %s", url, error.code)
        except URLError as error:
            logging.info("We failed to reach a server.")
            logging.info("Reason: %s", error.reason)

        return content
