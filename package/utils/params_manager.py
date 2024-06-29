import os
from typing import Union, Optional, Dict, Mapping

PM_TYPE_CACHE = "cache"
PM_TYPE_REDIS = "redis"

# to track the captcha related operations via persistency manager
CAPTCHA_UUID_KEY = 'captcha_uuid'

DEFAULT_EXPTIME = 90

# App default host & port
APP_HOST_CONFIG: dict = {
    "param_key": 'app_host',
    "param_env_name": 'PYCAP_APP_HOST',
    "default": '127.0.0.1'
}
APP_PORT_CONFIG: dict = {
    "param_key": 'app_port',
    "param_env_name": 'PYCAP_APP_PORT',
    "default": "8000"
}
# PM configs
APP_PM_CLASS: dict = {
    "param_key": 'pm_class',
    "param_env_name": 'PYCAP_PM_CLASS',
    "default": PM_TYPE_REDIS
}
# Local Cache PM configs
APP_PM_CACHE_EXPTIME: Dict[str, Union[str, int]] = {
    "param_key": 'expire_time_s',
    "param_env_name": 'PYCAP_PM_CACHE_EXPTIME',
    "default": DEFAULT_EXPTIME
}
APP_PM_CACHE_TIDYTIME: Dict[str, Union[str, int]] = {
    "param_key": 'tidy_time_s',
    "param_env_name": 'PYCAP_PM_CACHE_TIDYTIME',
    "default": 10
}
# Redis PM configs
APP_PM_REDIS_HOST: dict = {
    "param_key": 'host',
    "param_env_name": 'PYCAP_APP_REDIS_HOST',
    "default": '127.0.0.1'
}
APP_PM_REDIS_PORT: Dict[str, Union[str, int]] = {
    "param_key": 'port',
    "param_env_name": 'PYCAP_APP_REDIS_PORT',
    "default": 6379
}
APP_PM_REDIS_EXPTIME: Dict[str, Union[str, int]] = {
    "param_key": 'expire_time_s',
    "param_env_name": 'PYCAP_PM_REDIS_EXPTIME',
    "default": DEFAULT_EXPTIME
}
APP_PM_REDIS_DECODE_RESP: Dict[str, Union[str, bool]] = {
    "param_key": 'decode_responses',
    "param_env_name": 'PYCAP_PM_REDIS_DECODE_RESP',
    "default": True
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
    # print(param_key, param_env_name, default, params_dict)
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
    response = retrieve_parameter(**APP_HOST_CONFIG)
    return None if response is None else str(response)

def get_app_port() -> Optional[int]:
    response = retrieve_parameter(**APP_PORT_CONFIG)
    return None if response is None else int(response)

def get_pm_params(pm_class: str) -> dict:
    if pm_class == PM_TYPE_CACHE:
        return retrieve_multiple_params(PM_CACHE_PARAMS)
    if pm_class == PM_TYPE_REDIS:
        return retrieve_multiple_params(PM_REDIS_PARAMS)
    return {}
