import os
from sys import argv
import logging
from waitress import serve
from paste.translogger import TransLogger
from usage import create_spa

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app_with_logger = TransLogger(create_spa(), setup_console_handler=False)

# https://stackoverflow.com/questions/11087682/does-gunicorn-run-on-windows

# Resolve the port we're using

try:
    index = argv.index('--port')
    port = argv[index+1]
except Exception:
    port = int(os.environ.get("PORT", 8050))

hostname = os.environ.get("HOST_HOSTNAME", "localhost")
hostport = os.environ.get("HOST_HOSTPORT", "8050")

print(f' * stock-server V{"0.0.1"}')
print(f' * Visit http://{hostname}:{hostport}/admin/login\n')

serve(app_with_logger, port=port)
