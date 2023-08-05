# ravi_utils

Simple utilities for quick scripts

## Install 

    pip install ravi_utils

## Sample usage

    # -*- coding: utf-8 -*-

    import logging
    import sys

    from ravi_utils.common import CommonOps
    from ravi_utils.common_logging import LogOps
    from ravi_utils.common_conf import ConfOps

    def main():
        """Main function"""

        LogOps.setup_logging("./log", "main", logging.DEBUG)
        CommonOps.param_check(1)
        conf = ConfOps.init_conf(sys.argv[1], [
            "some_option"
        ])

        logging.info("start one")
        logging.debug("conf value: " + conf["some_option"])

    if __name__ == '__main__':
        main()

