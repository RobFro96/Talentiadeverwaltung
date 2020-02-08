import logging

import coloredlogs

from util.error_collector import ErrorCollector

coloredlogs.install(fmt='%(asctime)s,%(msecs)d %(levelname)-5s '
                    '[%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)


logging.info("Hallo Welt!")
logging.error("Test!")

ec = ErrorCollector()
logging.info("hi! %s", "data")
logging.error("Error!")
ec.show_messagebox()
