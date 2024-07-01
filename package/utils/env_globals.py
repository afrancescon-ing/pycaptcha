import logging
import os
from typing import Union, Dict
from package.persistency.prims import pm_factory
from package.utils.params_manager import \
    get_captcha_width,\
    get_captcha_height,\
    get_textgen_allowed_chars,\
    get_textgen_length
from package.persistency.managers.cache_local_pm import LocalCachePersistenceManager
from package.persistency.managers.redis_pm import RedisPersistenceManager

logger = logging.getLogger(__name__)

persistence_manager: Union[LocalCachePersistenceManager, RedisPersistenceManager]
captcha_width: int
captcha_height: int
textgen_length: int
textgen_allowed_chars: str

def init_environment(env_vars: Union[Dict[str, str], None] =None):
    global persistence_manager 
    global captcha_width
    global captcha_height
    global textgen_length
    global textgen_allowed_chars

    if env_vars is None:
        env_vars = {}
    for env_var, value in env_vars.items():
        os.environ[env_var] = value

    persistence_manager = pm_factory()
    captcha_width = get_captcha_width()
    captcha_height = get_captcha_height()
    textgen_length = get_textgen_length()
    textgen_allowed_chars = get_textgen_allowed_chars()
    logger.info("[APP] Environment Initialised:"
                "\n\tcaptcha_width= %i"
                "\n\tcaptcha_height= %i"
                "\n\ttextgen_length= %i"
                "\n\ttextgen_allowed_chars= '%s'",
                captcha_width,
                captcha_height,
                textgen_length,
                textgen_allowed_chars)

def get_pm_type() -> str:
    return persistence_manager.my_type()
    