"""
    Constant definitions
    
    Naming convention
    <COMPONENT>_<PNAME1>_<PNAME...>_<PNAMEX>_<CONTEXT> 
    
    Context suffixes meaning:
    _KEY:       key name in dictionaries
    _ENV:       environment variable name
    _DEFAULT:   default value
"""

PM_CACHE_TYPE= "cache"
PM_REDIS_TYPE = "redis"

PM_EXPTIME_DEFAULT = 90

### PM configs
PM_CLASS_KEY = 'pm_class'
PM_CLASS_ENV = 'PYCAP_PM_CLASS'
PM_CLASS_DEFAULT = PM_CACHE_TYPE

### Local Cache PM 

# Expiration time interval for a cache entry
PM_CACHE_EXPTIME_KEY = 'expire_time_s'
PM_CACHE_EXPTIME_ENV = 'PYCAP_PM_CACHE_EXPTIME'
PM_CACHE_EXPTIME_DEFAULT = PM_EXPTIME_DEFAULT

# Tidy time interval
PM_CACHE_TIDYTIME_KEY = 'tidy_time_s'
PM_CACHE_TIDYTIME_ENV = 'PYCAP_PM_CACHE_TIDYTIME'
PM_CACHE_TIDYTIME_DEFAULT = 10

### Redis PM

PM_REDIS_HOST_KEY = 'host'
PM_REDIS_HOST_ENV = 'PYCAP_APP_REDIS_HOST'
PM_REDIS_HOST_DEFAULT = '127.0.0.1'

PM_REDIS_PORT_KEY = 'port'
PM_REDIS_PORT_ENV = 'PYCAP_APP_REDIS_PORT'
PM_REDIS_PORT_DEFAULT = 6379

# Expiration time interval for a redis key
PM_REDIS_EXPTIME_KEY = 'expire_time_s'
PM_REDIS_EXPTIME_ENV = 'PYCAP_PM_REDIS_EXPTIME'
PM_REDIS_EXPTIME_DEFAULT = PM_EXPTIME_DEFAULT


PM_REDIS_DECODE_RESP_KEY = 'expire_time_s'
PM_REDIS_DECODE_RESP_ENV = 'PYCAP_PM_REDIS_DECODE_RESP'
PM_REDIS_DECODE_RESP_DEFAULT = True
