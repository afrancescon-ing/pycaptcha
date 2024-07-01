import logging
from time import time
from multiprocessing import Lock
from threading import Timer
from package.persistency.managers.pm_interface import PersistenceManagerInterface
from package.persistency.managers import PM_CACHE_TYPE
from package.utils.params_manager import get_app_host, get_app_port

CACHE_VALUE = 0
CACHE_TIME = 1

CACHE_TIDY_INTERVAL = 15

logger = logging.getLogger(__name__)

class LocalCachePersistenceManager(PersistenceManagerInterface):
    """ Persistance Manager implemented as Local Cache (dictionary)
    """

    def __init__(self, expire_time_s: int, tidy_time_s: int):
        super().__init__()
        self._lock = Lock()
        self._cache: dict = {}
        self.expire_time_s: int = expire_time_s
        self.tidy_time_s: int = tidy_time_s
        self.app_host = get_app_host()
        self.app_port = get_app_port()
        self.schedule_tidings()
        logger.info("[CACHE_PM] Initialised:"
                    "\n\texpire_time= %is"
                    "\n\ttidy_time= %is",
                    self.expire_time_s,
                    self.tidy_time_s)
        # self.scheduler = sched.scheduler(time, sleep)
        # self.scheduler.enter(CACHE_TIDY_INTERVAL, 1, tidy_routine, (self,))
        # self.scheduler.run()

    def push(self, uuid: str, value: str):
        self._lock.acquire()
        try:
            if uuid in self._cache:
                return False
            self._cache[uuid] = [value, time()]
            # print("Insertion response %s/%s",uuid, value)
            logger.debug(
                '[CACHE_PM] ADDED new captcha @%s:%i/%s/%s',
                self.app_host,
                self.app_port,
                uuid,
                value)
            return True
        finally:
            self._lock.release()

    def pop(self, uuid: str):
        self._lock.acquire()
        try:
            response =  self._cache.pop(uuid)[CACHE_VALUE]
            # print("DEleteion response %s",response)
            logger.debug(
                '[CACHE_PM] DELETED captcha @%s:%i/%s/%s',
                self.app_host,
                self.app_port,
                uuid,
                response)
            return response
        except KeyError:
            return None
        finally:
            self._lock.release()

    def tidy(self):
        self._lock.acquire()
        try:
            now = time()
            expired = []
            anomalies = []
            kept = []
            for key, entry in self._cache.items():
                if now - entry[CACHE_TIME] >= self.expire_time_s:
                    expired.append(key)
                else:
                    kept.append(key)
            for uuid in expired:
                try:
                    self._cache.pop(uuid)
                except KeyError:
                    anomalies.append(uuid)
            return (kept, expired, anomalies)
        finally:
            self._lock.release()

    def schedule_tidings(self):
        # self.scheduler.enter(CACHE_TIDY_INTERVAL, 1, tidy_routine, (self,))
        t = Timer(self.tidy_time_s, self.tidy_routine, [])
        t.daemon = True
        t.start()

    def tidy_routine(self):
        self.schedule_tidings()
        self.print_tidy_report(*self.tidy())

    def print_tidy_report(self, kept, expired, anomalies):
        logger.debug('[CACHE_PM] Tidy report: '
                     'original %i, kept: %i '
                     '(expired&deleted: %i - deletion anomalies: %i)',
                     len(kept)+len(expired),
                     len(kept),
                     len(expired),
                     len(anomalies))

    def my_type(self) -> str:
        return PM_CACHE_TYPE

# def tidy_routine(cache_pm: LocalCachePersistenceManager):
#     cache_pm.schedule_tidings()
#     logger.debug(cache_pm.tidy())
