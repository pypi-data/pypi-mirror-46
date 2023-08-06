import logging
import os

name = 'frd_logging'
LOG_DIR = 'logfile'
DEFAULT_FORMATTER = '%(asctime)s : %(levelname)s : %(name)s %(message)s'


def get_logger():
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    filename = LOG_DIR + '/logger.log'
    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    logging.basicConfig(filename=filename,
                        level=logging.DEBUG,
                        format=DEFAULT_FORMATTER)
    return logger