from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET, FATAL, WARN
import logging
from .spa_config import config

options = config.get('logging')

def getOptionsLevel(default='WARN'):
    return options.get('level', default_value=default)

logging.basicConfig(
    level = getOptionsLevel(),
    # format = '%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    format = '%(levelname)s %(module)13s/%(lineno)-5d %(message)s'
)

log = logging.getLogger("dash_spa")

def getLogger(name=None):
    return logging.getLogger(name)

def setLevel(level):
    log.setLevel(level=level)