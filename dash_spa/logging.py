from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET, FATAL, WARN
import logging

logging.basicConfig(
    level = "WARNING",
    # format = '%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    format = '%(levelname)s %(module)13s/%(lineno)-5d %(message)s'
)

log = logging.getLogger(__name__)

def getLogger(name=None):
    return logging.getLogger(name)

def setLevel(level):
    log.setLevel(level=level)