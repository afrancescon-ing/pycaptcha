""" Utility functions for persistence management
"""

import logging
import os
from typing import Optional, Union
from package.persistency.managers.cache_local_pm import LocalCachePersistenceManager
from package.persistency.managers.redis_pm import RedisPersistenceManager
from package.utils.params_manager import \
    PM_CACHE_TYPE,\
    PM_REDIS_TYPE,\
    get_pm_class,\
    get_pm_params

logger = logging.getLogger(__name__)

def get_parameter(param: str, param_dict: Optional[dict] =None, 
                  param_env_name: Optional[str] =None, 
                  default:  Union[str, int, float, bool, None] =None):
    """Return the value of a given parameter, according to passed parameters

    Args:
        param (str): parameter key (=ientifier)
        param_dict (Optional[dict], optional): dictionary listing parameters.
                                               Defaults to None.
        param_env_name (Optional[str], optional): name of the env var related 
                                                  to param. Defaults to None.
        default (Union[str, int, float, None], optional): param's default value
                                                          Defaults to None.

    Returns:
        Union (str | int | float | bool | None): parameter's value
    """
    if param_dict and param in param_dict:
        return param_dict[param]
    elif param_env_name:
        return os.environ[param_env_name]
    else:
        return default

def pm_factory_none_allowed(
    pmanager_type: str,
    params: Optional[dict] =None) -> \
    Union[LocalCachePersistenceManager, RedisPersistenceManager, None]:
    if params is None:
        params = {}
    if pmanager_type == PM_CACHE_TYPE:
        return LocalCachePersistenceManager(**params)
    elif pmanager_type == PM_REDIS_TYPE:
        return RedisPersistenceManager(**params)

    return None

def pm_factory(
    pmanager_type: Optional[str] =None,
    params: Optional[dict] =None) -> \
    Union[LocalCachePersistenceManager, RedisPersistenceManager]:
    """Returns a PM instance according to arguments

    Args:
        pmanager_type (Optional[str], optional): PM type. Defaults to None.
        params (Optional[dict], optional): PM configuration params. 
                                           Defaults to None.

    Raises:
        ValueError: Persistence Manager is not assigned

    Returns:
        Union (LocalCachePersistenceManager | RedisPersistenceManager): PM instance
    """
    if pmanager_type is None:
        # get default value for PM class
        pmanager_type = get_pm_class()
    if params is None:
        # get env var/default values for PM config
        params = get_pm_params(pmanager_type)
    pm = pm_factory_none_allowed(pmanager_type, params)
    if pm is None:
        raise ValueError("Persistence Manager is not assigned")
    return pm
