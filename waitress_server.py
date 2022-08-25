import os
from sys import argv
from waitress import serve
from paste.translogger import TransLogger
from app import create_dash
from usage import create_app
from dash_spa import __version__, logging, config

options = config.get('logging')

logging.setLevel(options.level)

logger = logging.getLogger('waitress')
logger.setLevel(logging.WARN)

_log = logging.getLogger('redux_store')
_log.setLevel(logging.INFO)

app = create_app(create_dash)

app_with_logger = TransLogger(app.server, setup_console_handler=False)

try:
    index = argv.index('--port')
    port = argv[index+1]
except Exception:
    port = int(os.environ.get("PORT", 5000))

print(f'DashSPA V{__version__}')

# serve(app_with_logger, host='0.0.0.0', port=port)

serve(app.server, host='0.0.0.0', port=port)
