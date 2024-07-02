""" Utility functions for logger configuration
"""

import logging
import os
from datetime import datetime
from package import LOG_LEVEL_DEFAULT,\
                    LOG_LOGFILENAME_TIMEZONE_DEFAULT, \
                    LOG_LOGFILENAME_PREFIX_DEFAULT, \
                    LOG_LOGFILENAME_TIMEFORMAT_DEFAULT, \
                    LOG_LOGFOLDER_DEFAULT,\
                    LOG_FORMAT_DEFAULT,\
                    LOG_DATEFORMAT_DEFAULT
                    

def configure_log():
    """ Log configuration
    """

    if not os.path.exists(LOG_LOGFOLDER_DEFAULT+'/'):
        os.makedirs(LOG_LOGFOLDER_DEFAULT+'/')

    timeref = datetime.now(LOG_LOGFILENAME_TIMEZONE_DEFAULT)\
                      .strftime(LOG_LOGFILENAME_TIMEFORMAT_DEFAULT)

    logfilename = f'{LOG_LOGFOLDER_DEFAULT}/{LOG_LOGFILENAME_PREFIX_DEFAULT}_{timeref}.log'

    logging.basicConfig(
        format=LOG_FORMAT_DEFAULT,
        datefmt=LOG_DATEFORMAT_DEFAULT,
        level=LOG_LEVEL_DEFAULT,
        handlers=[
            logging.FileHandler(logfilename),
            logging.StreamHandler()
        ])
    