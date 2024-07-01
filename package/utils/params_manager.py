import os
from enum import Enum
from typing import Union, Optional, Dict
from package import \
    APP_HOST_KEY,\
    APP_HOST_ENV,\
    APP_HOST_DEFAULT,\
    APP_PORT_KEY,\
    APP_PORT_ENV,\
    APP_PORT_DEFAULT,\
    CAPTCHA_IMAGE_WIDTH_KEY,\
    CAPTCHA_IMAGE_WIDTH_ENV,\
    CAPTCHA_IMAGE_WIDTH_DEFAULT,\
    CAPTCHA_IMAGE_HEIGHT_KEY,\
    CAPTCHA_IMAGE_HEIGHT_ENV,\
    CAPTCHA_IMAGE_HEIGHT_DEFAULT,\
    TEXTGEN_ALLOWED_CHARS_KEY,\
    TEXTGEN_ALLOWED_CHARS_ENV,\
    TEXTGEN_ALLOWED_CHARS_DEFAULT,\
    TEXTGEN_LENGTH_KEY,\
    TEXTGEN_LENGTH_ENV,\
    TEXTGEN_LENGTH_DEFAULT
    
from package.persistency.managers import \
    PM_CLASS_KEY,\
    PM_CLASS_ENV,\
    PM_CLASS_DEFAULT,\
    PM_CACHE_EXPTIME_KEY,\
    PM_CACHE_EXPTIME_ENV,\
    PM_CACHE_EXPTIME_DEFAULT,\
    PM_CACHE_TIDYTIME_KEY,\
    PM_CACHE_TIDYTIME_ENV,\
    PM_CACHE_TIDYTIME_DEFAULT,\
    PM_REDIS_HOST_KEY,\
    PM_REDIS_HOST_ENV,\
    PM_REDIS_HOST_DEFAULT,\
    PM_REDIS_PORT_KEY,\
    PM_REDIS_PORT_ENV,\
    PM_REDIS_PORT_DEFAULT,\
    PM_REDIS_EXPTIME_KEY,\
    PM_REDIS_EXPTIME_ENV,\
    PM_REDIS_EXPTIME_DEFAULT,\
    PM_REDIS_DECODE_RESP_KEY,\
    PM_REDIS_DECODE_RESP_ENV,\
    PM_REDIS_DECODE_RESP_DEFAULT,\
    PM_CACHE_TYPE,\
    PM_REDIS_TYPE 
    
class ParamType(Enum):
    INT = 'int',
    FLOAT = 'float'
    STR = 'str',
    BOOL = 'bool',
    NONE = 'None'
    

# App default host & port
APP_HOST: dict = {
    "param_key": APP_HOST_KEY,
    "param_env_name": APP_HOST_ENV,
    "default": str(APP_HOST_DEFAULT),
    "param_type": ParamType.STR
}
APP_PORT: dict = {
    "param_key": APP_PORT_KEY,
    "param_env_name": APP_PORT_ENV,
    "default": str(APP_PORT_DEFAULT),
    "param_type": ParamType.INT
}

# Captch width and height
CAPTCHA_IMAGE_WIDTH: dict = {
    "param_key": CAPTCHA_IMAGE_WIDTH_KEY,
    "param_env_name": CAPTCHA_IMAGE_WIDTH_ENV,
    "default": str(CAPTCHA_IMAGE_WIDTH_DEFAULT),
    "param_type": ParamType.INT
}
CAPTCHA_IMAGE_HEIGHT: dict = {
    "param_key": CAPTCHA_IMAGE_HEIGHT_KEY,
    "param_env_name": CAPTCHA_IMAGE_HEIGHT_ENV,
    "default": str(CAPTCHA_IMAGE_HEIGHT_DEFAULT),
    "param_type": ParamType.INT
}

# Textgen
TEXTGEN_ALLOWED_CHARS: dict = {
    "param_key": TEXTGEN_ALLOWED_CHARS_KEY,
    "param_env_name": TEXTGEN_ALLOWED_CHARS_ENV,
    "default": str(TEXTGEN_ALLOWED_CHARS_DEFAULT),
    "param_type": ParamType.STR
}

TEXTGEN_LENGTH: dict = {
    "param_key": TEXTGEN_LENGTH_KEY,
    "param_env_name": TEXTGEN_LENGTH_ENV,
    "default": str(TEXTGEN_LENGTH_DEFAULT),
    "param_type": ParamType.INT
}

# PM configs
APP_PM_CLASS: dict = {
    "param_key": PM_CLASS_KEY,
    "param_env_name": PM_CLASS_ENV,
    "default": str(PM_CLASS_DEFAULT),
    "param_type": ParamType.STR
}
# Local Cache PM configs
APP_PM_CACHE_EXPTIME: dict = {
    "param_key": PM_CACHE_EXPTIME_KEY,
    "param_env_name": PM_CACHE_EXPTIME_ENV,
    "default": str(PM_CACHE_EXPTIME_DEFAULT),
    "param_type": ParamType.INT
}
APP_PM_CACHE_TIDYTIME: dict = {
    "param_key": PM_CACHE_TIDYTIME_KEY,
    "param_env_name": PM_CACHE_TIDYTIME_ENV,
    "default": str(PM_CACHE_TIDYTIME_DEFAULT),
    "param_type": ParamType.INT
}
# Redis PM configs
APP_PM_REDIS_HOST: dict = {
    "param_key": PM_REDIS_HOST_KEY,
    "param_env_name": PM_REDIS_HOST_ENV,
    "default": str(PM_REDIS_HOST_DEFAULT),
    "param_type": ParamType.STR
}
APP_PM_REDIS_PORT: dict = {
    "param_key": PM_REDIS_PORT_KEY,
    "param_env_name": PM_REDIS_PORT_ENV,
    "default": str(PM_REDIS_PORT_DEFAULT),
    "param_type": ParamType.INT
}
APP_PM_REDIS_EXPTIME: dict = {
    "param_key": PM_REDIS_EXPTIME_KEY,
    "param_env_name": PM_REDIS_EXPTIME_ENV,
    "default": str(PM_REDIS_EXPTIME_DEFAULT),
    "param_type": ParamType.INT
}
APP_PM_REDIS_DECODE_RESP: dict = {
    "param_key": PM_REDIS_DECODE_RESP_KEY,
    "param_env_name": PM_REDIS_DECODE_RESP_ENV,
    "default": str(PM_REDIS_DECODE_RESP_DEFAULT),
    "param_type": ParamType.BOOL
}

PM_CACHE_PARAMS = [
    APP_PM_CACHE_EXPTIME,
    APP_PM_CACHE_TIDYTIME]

PM_REDIS_PARAMS = [
    APP_PM_REDIS_DECODE_RESP,
    APP_PM_REDIS_EXPTIME,
    APP_PM_REDIS_HOST,
    APP_PM_REDIS_PORT]

def typize(value=str, desired_type=str) -> Union[ str, int, float, bool, None]:
    if desired_type == ParamType.STR:
        return str(value)
    if desired_type == ParamType.INT:
        return int(value)
    if desired_type == ParamType.FLOAT:
        return float(value)
    if desired_type == ParamType.BOOL:
        return bool(value)
    if desired_type == ParamType.NONE:
        return None
    raise ValueError(f'invalid desired_type: {desired_type}')

def retrieve_parameter( 
        param_key: str, 
        param_env_name: Union[str , None] =None,
        default: Union[str, None] =None,
        param_type: Union[str, ParamType] =ParamType.STR,
        params_dict: Union[Dict[str, Union[ str, int, float, bool, None]], None] =None) -> \
        Union[ str, int, float, bool, None]:
    print(param_key, param_env_name, default, params_dict)
    if params_dict and param_key in params_dict:
        return typize(params_dict[param_key], param_type)

    if param_env_name:
        try:
            return typize(os.environ[param_env_name], param_type)
        except KeyError:
            pass

    return typize(default, param_type)

def retrieve_multiple_params(Params_desc_list: list) -> dict:
    params = {}
    for param_desc in Params_desc_list:
        params[param_desc["param_key"]] = retrieve_parameter(**param_desc)
    return params

def get_pm_class() -> str:
    response = retrieve_parameter(**APP_PM_CLASS)
    if response is None:
        raise TypeError("Persistence Manager class shall be a string (not None)")
    return str(response)

def get_app_host() -> Optional[str]:
    response = retrieve_parameter(**APP_HOST)
    return None if response is None else str(response)

def get_app_port() -> Optional[int]:
    response = retrieve_parameter(**APP_PORT)
    return None if response is None else int(response)

def get_pm_params(pm_class: str) -> dict:
    if pm_class == PM_CACHE_TYPE:
        return retrieve_multiple_params(PM_CACHE_PARAMS)
    if pm_class == PM_REDIS_TYPE:
        return retrieve_multiple_params(PM_REDIS_PARAMS)
    return {}

def get_captcha_width() -> int:
    response = retrieve_parameter(**CAPTCHA_IMAGE_WIDTH)
    return CAPTCHA_IMAGE_WIDTH_DEFAULT if response is None else int(response)

def get_captcha_height() -> int:
    response = retrieve_parameter(**CAPTCHA_IMAGE_HEIGHT)
    return CAPTCHA_IMAGE_HEIGHT_DEFAULT if response is None else int(response)

def get_textgen_allowed_chars() -> str:
    response = retrieve_parameter(**TEXTGEN_ALLOWED_CHARS)
    return '' if response is None else str(response)

def get_textgen_length() -> int:
    response = retrieve_parameter(**TEXTGEN_LENGTH)
    return 0 if response is None else int(response)

def get_cache_tidytime() -> int:
    response = retrieve_parameter(**APP_PM_CACHE_TIDYTIME)
    return 0 if response is None else int(response)

def get_redis_exptime() -> int:
    response = retrieve_parameter(**APP_PM_REDIS_EXPTIME)
    return 0 if response is None else int(response)