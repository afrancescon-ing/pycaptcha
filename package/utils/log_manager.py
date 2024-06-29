import logging
import os
from datetime import datetime, timezone

def configure_log():

    if not os.path.exists("log/"):
        os.makedirs("log/")

    timeref = datetime.now(timezone.utc).strftime('%Y-%m-%d-%H-%M-%S')

    logfilename = f'log/pycap_{timeref}.log'

    logging.basicConfig(
        format='[%(asctime)s,%(msecs)d %(name)s %(levelname)s] {%(message)s}',
        datefmt='%Z %Y-%m-%d %H:%M:%S',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(logfilename),
            logging.StreamHandler()
        ])
    