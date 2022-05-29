import os
from sys import argv
from waitress import serve
from dash_spa import logging

from paste.translogger import TransLogger

from .app import create_app, create_dash


app = create_app(create_dash)
app_with_logger = TransLogger(app.server, setup_console_handler=False)


# python -m examples.storage_test.waitress_server

if __name__ == "__main__":
    logging.setLevel("INFO")

    port = int(os.environ.get("PORT", 5000))
    hostname = os.environ.get("HOSTNAME", "localhost")
    hostport = os.environ.get("HOSTPORT", "5000")

    print(f' * Visit http://{hostname}:{hostport}')
    serve(app.server, host='0.0.0.0', port=port)
