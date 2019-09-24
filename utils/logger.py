import logging

from utils import config

log_options = config.get('logging')

logging.basicConfig(
    level=log_options.level,
    # format='%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    format='%(levelname)s %(module)10s/%(lineno)-5d %(message)s'
)

log = logging.getLogger()
