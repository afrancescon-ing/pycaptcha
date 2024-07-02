""" Persistance Manager implemented as Redis
"""

import logging
from typing import Optional
import redis
from package.persistency.managers.pm_interface import PersistenceManagerInterface
from package.persistency.managers import PM_REDIS_TYPE
from package.utils.params_manager import get_app_host, get_app_port

REDIS_SET_ONLY_IF_NOT_EXISTENT = True
REDIS_SET_OK_RESPONSE = 'OK'
REDIS_SET_KO_RESPONSE = 'nil'
REDIS_EXPIRE_OK_RESPONSE = 1
REDIS_EXPIRE_KO_RESPONSE = 0

logger = logging.getLogger(__name__)

class RedisPersistenceManager(PersistenceManagerInterface):
    """ Persistance Manager implemented as Redis
    """

    def __init__(self, host: str='localhost', port: int=6379,
                 decode_responses: bool=True, expire_time_s: int=90):
        self.host = host
        self.port = port
        self.decode_responses = decode_responses
        self.expire_time_s = expire_time_s
        self.app_host = get_app_host()
        self.app_port = get_app_port()
        # self._redis_connection: Optional[redis.Redis] = None
        self._connect()
        logger.info("[REDIS_PM] Initialised: "
                    "\n\thost&port= %s:%i"
                    "\n\tdecode_responses= %s"
                    "\n\texpire_time= %is"
                    "\n\tconnected= %s",
                    self.host,
                    self.port,
                    self.decode_responses,
                    self.expire_time_s,
                    True if self._redis_connection else False)

    def _connect(self) -> None:
        self._redis_connection = redis.Redis(
            self.host, self.port, 
            decode_responses=self.decode_responses)

    def push_original(self, uuid: str, value: str) -> bool:
        """Performing a push into Redis

        Args:
            uuid (str): captcha's uuid
            value (str): captcha's associated text

        Returns:
            bool: if insertion was successful or not
        """
        response= self._redis_connection.set(
            uuid, value, ex=self.expire_time_s,
            nx=REDIS_SET_ONLY_IF_NOT_EXISTENT)

        if response:
            logger.debug(
                '[REDIS_PM] ADDED new captcha @%s:%i/%s/%s',
                self.app_host,
                self.app_port,
                uuid,
                value)

        return bool(response)

    def pop_original(self, uuid: str) -> Optional[str]:
        """Performing a pop on Redis

        Args:
            uuid (str): captcha's uuid

        Returns:
            Union (str | None): captcha's associated value (on success) or None
        """
        response = self._redis_connection.getdel(uuid)

        if response:
            logger.debug(
                '[REDIS_PM] DELETED captcha @%s:%i/%s/%s',
                self.app_host,
                self.app_port,
                uuid,
                response)
            return str(response)
        return None

    def push(self, uuid: str, value: str) -> bool:
        return self.push_original(uuid, value)

    def pop(self, uuid: str) -> Optional[str]:
        return self.pop_original(uuid)

    def my_type(self) -> str:
        return PM_REDIS_TYPE
