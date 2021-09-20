import logging

from usage import create_spa


if __name__ == "__main__":

    app = create_spa()

    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    app.run(debug=False, threaded=False)
