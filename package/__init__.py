"""
    Constant definitions
    
    Naming convention
    <COMPONENT>_<PNAME1>_<PNAME...>_<PNAMEX>_<CONTEXT> 
    
    Context suffixes meaning:
    _KEY:       key name in dictionaries
    _ENV:       environment variable name
    _DEFAULT:   default value
"""

import logging
from string import ascii_uppercase
from datetime import timezone

### APP

APP_HOST_KEY = 'app_host'
APP_HOST_ENV = 'PYCAP_APP_HOST'
APP_HOST_DEFAULT = '0.0.0.0'

APP_PORT_KEY = 'app_port'
APP_PORT_ENV = 'PYCAP_APP_PORT'
APP_PORT_DEFAULT = 8000

### LOG

# Log level
LOG_LEVEL_KEY = 'log_level'
LOG_LEVEL_ENV = 'PYCAP_LOG_LEVEL'
LOG_LEVEL_DEFAULT = logging.DEBUG

# Folder where log files are saved
LOG_LOGFOLDER_KEY = 'log_logfolder'
LOG_LOGFOLDER_ENV = 'PYCAP_LOG_LOGFOLDER'
LOG_LOGFOLDER_DEFAULT = 'log'

# Other log configs
LOG_LOGFILENAME_PREFIX_DEFAULT = 'pycap'
LOG_LOGFILENAME_TIMEFORMAT_DEFAULT = '%Y-%m-%d-%H-%M-%S'
LOG_LOGFILENAME_TIMEZONE_DEFAULT = timezone.utc
LOG_FORMAT_DEFAULT = '[%(asctime)s,%(msecs)d %(name)s %(levelname)s] {%(message)s}'
LOG_DATEFORMAT_DEFAULT = '%Z %Y-%m-%d %H:%M:%S'

### TEXTGEN

# Fixed length for a generated string
TEXTGEN_LENGTH_KEY = 'textgen_length'
TEXTGEN_LENGTH_ENV = 'PYCAP_TEXTGEN_LENGTH'
TEXTGEN_LENGTH_DEFAULT = 10


# String of all allowed chars in generated string
TEXTGEN_ALLOWED_CHARS_KEY = 'textgen_allowed_chars'
TEXTGEN_ALLOWED_CHARS_ENV = 'PYCAP_TEXTGEN_ALLOWED_CHARS'
TEXTGEN_ALLOWED_CHARS_DEFAULT = ascii_uppercase

### CAPTCHA

CAPTCHA_IMAGE_WIDTH_KEY = 'captcha_width'
CAPTCHA_IMAGE_WIDTH_ENV = 'PYCAP_CAPTCHA_WIDTH'
CAPTCHA_IMAGE_WIDTH_DEFAULT = 280

CAPTCHA_IMAGE_HEIGHT_KEY = 'captcha_height'
CAPTCHA_IMAGE_HEIGHT_ENV = 'PYCAP_CAPTCHA_HEIGHT'
CAPTCHA_IMAGE_HEIGHT_DEFAULT = 100

# Key used in the response header of "generate" endpoint
CAPTCHA_UUID_KEY = 'captcha_uuid'
