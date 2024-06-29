import logging
import os
from typing import Optional, Union
from package.persistency.managers.cache_local_pm import LocalCachePersistenceManager
from package.persistency.managers.redis_pm import RedisPersistenceManager
from package.utils.params_manager import PM_TYPE_CACHE, PM_TYPE_REDIS, get_pm_class, get_pm_params

PYCAP_REDIS_HOST = 'PYCAP_REDIS_HOST'
PYCAP_REDIS_PORT = 'PYCAP_REDIS_PORT'
PYCAP_REDIS_DECODE_RESPONSE = 'PYCAP_REDIS_DECODE_RESPONSE'
PYCAP_REDIS_EXPIRE_TIME_S = 'PYCAP_REDIS_EXPIRE_TIME_S'



logger = logging.getLogger(__name__)

def get_parameter(param: str, param_dict: Optional[dict] =None, param_env_name: Optional[str] =None, default:  Union[str, int, float, None] =None):
    if param_dict and param in param_dict:
        return param_dict[param]
    elif param_env_name:
        return os.environ[param_env_name]
    else:
        return default

def pm_factory_none_allowed(pmanager_type: str, params: Optional[dict] =None) -> Union[LocalCachePersistenceManager, RedisPersistenceManager, None]:
    if params is None:
        params = {}
    if pmanager_type == PM_TYPE_CACHE:
        return LocalCachePersistenceManager(**params)
    elif pmanager_type == PM_TYPE_REDIS:
        return RedisPersistenceManager(**params)
    
    return None

def pm_factory(pmanager_type: Optional[str] =None, params: Optional[dict] =None) -> Union[LocalCachePersistenceManager, RedisPersistenceManager]:
    if pmanager_type is None:
        pmanager_type = get_pm_class()
    if params is None:
        params = get_pm_params(pmanager_type)
    pm = pm_factory_none_allowed(pmanager_type, params)
    if pm is None:
        raise TypeError("Persistence Manager is not assigned")
    return pm
    
