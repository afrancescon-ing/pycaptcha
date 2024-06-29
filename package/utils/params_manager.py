import os
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
    CAPTCHA_IMAGE_HEIGHT_DEFAULT
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

# App default host & port
APP_HOST: dict = {
    "param_key": APP_HOST_KEY,
    "param_env_name": APP_HOST_ENV,
    "default": APP_HOST_DEFAULT
}
APP_PORT: dict = {
    "param_key": APP_PORT_KEY,
    "param_env_name": APP_PORT_ENV,
    "default": APP_PORT_DEFAULT
}

# Captch width and height
CAPTCHA_IMAGE_WIDTH: dict = {
    "param_key": CAPTCHA_IMAGE_WIDTH_KEY,
    "param_env_name": CAPTCHA_IMAGE_WIDTH_ENV,
    "default": CAPTCHA_IMAGE_WIDTH_DEFAULT
}
CAPTCHA_IMAGE_HEIGHT: dict = {
    "param_key": CAPTCHA_IMAGE_HEIGHT_KEY,
    "param_env_name": CAPTCHA_IMAGE_HEIGHT_ENV,
    "default": CAPTCHA_IMAGE_HEIGHT_DEFAULT
}

# PM configs
APP_PM_CLASS: dict = {
    "param_key": PM_CLASS_KEY,
    "param_env_name": PM_CLASS_ENV,
    "default": PM_CLASS_DEFAULT
}
# Local Cache PM configs
APP_PM_CACHE_EXPTIME: Dict[str, Union[str, int]] = {
    "param_key": PM_CACHE_EXPTIME_KEY,
    "param_env_name": PM_CACHE_EXPTIME_ENV,
    "default": PM_CACHE_EXPTIME_DEFAULT
}
APP_PM_CACHE_TIDYTIME: Dict[str, Union[str, int]] = {
    "param_key": PM_CACHE_TIDYTIME_KEY,
    "param_env_name": PM_CACHE_TIDYTIME_ENV,
    "default": PM_CACHE_TIDYTIME_DEFAULT
}
# Redis PM configs
APP_PM_REDIS_HOST: dict = {
    "param_key": PM_REDIS_HOST_KEY,
    "param_env_name": PM_REDIS_HOST_ENV,
    "default": PM_REDIS_HOST_DEFAULT
}
APP_PM_REDIS_PORT: Dict[str, Union[str, int]] = {
    "param_key": PM_REDIS_PORT_KEY,
    "param_env_name": PM_REDIS_PORT_ENV,
    "default": PM_REDIS_PORT_DEFAULT
}
APP_PM_REDIS_EXPTIME: Dict[str, Union[str, int]] = {
    "param_key": PM_REDIS_EXPTIME_KEY,
    "param_env_name": PM_REDIS_EXPTIME_ENV,
    "default": PM_REDIS_EXPTIME_DEFAULT
}
APP_PM_REDIS_DECODE_RESP: Dict[str, Union[str, bool]] = {
    "param_key": PM_REDIS_DECODE_RESP_KEY,
    "param_env_name": PM_REDIS_DECODE_RESP_ENV,
    "default": PM_REDIS_DECODE_RESP_DEFAULT
}

PM_CACHE_PARAMS = [
    APP_PM_CACHE_EXPTIME,
    APP_PM_CACHE_TIDYTIME]

PM_REDIS_PARAMS = [
    APP_PM_REDIS_DECODE_RESP,
    APP_PM_REDIS_EXPTIME,
    APP_PM_REDIS_HOST,
    APP_PM_REDIS_PORT]

def retrieve_parameter( param_key: str, param_env_name: Union[str , None] =None, default: Union[ str, int, float, None] =None, params_dict: Union[Dict[str, Union[ str, int, float, None]], None] =None) -> Union[ str, int, float, None]:
    print(param_key, param_env_name, default, params_dict)
    if params_dict and param_key in params_dict:
        return params_dict[param_key]

    if param_env_name:
        try:
            return os.environ[param_env_name]
        except KeyError:
            pass

    return default

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
