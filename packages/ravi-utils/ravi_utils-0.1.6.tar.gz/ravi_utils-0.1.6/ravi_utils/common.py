# -*- coding: utf-8 -*-
"""Common function"""

import logging
import logging.handlers
import sys


class CommonOps:

    """Common functions"""

    @staticmethod
    def param_check(nr_of_params):
        """Checks if there is at least given number of parameters"""

        # First element in sys.argv is the program itself, so 2 is 1 parameter
        if len(sys.argv) < nr_of_params + 1:
            logging.info("Too few parameters: %s", nr_of_params)
            sys.exit(1)
