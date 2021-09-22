import os
from utils import log, logging

def serve_app(app, path=""):

    # Turn off werkzeug  logging as it's very noisy

    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    # Set SPA logging level (if needed)

    log.setLevel(logging.INFO)

    # When running in a Docker container the internal port
    # is mapped onto a host port. Use the env variables passed
    # in to the container to determin the host URL.

    port = int(os.environ.get("PORT", 8050))
    hostname = os.environ.get("HOST_HOSTNAME", "localhost")
    hostport = os.environ.get("HOST_HOSTPORT", "8050")

    print(f' * Visit http://{hostname}:{hostport}{path}')

    app.run(debug=False, host='0.0.0.0', port=port, threaded=False) 
