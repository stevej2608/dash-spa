import logging

from holoniq.utils import config

log_options = config.get('logging')

logging.basicConfig(
    level= "WARNING" if not hasattr(log_options,'level') else log_options.level,
    # format='%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    format='%(levelname)s %(module)10s/%(lineno)-5d %(message)s'
)

def set_level(level=None):
    if level:
        logging.basicConfig(level= level)


log = logging.getLogger()
