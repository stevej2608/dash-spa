from dataclasses import _process_class
from itsdangerous import Signer, BadSignature
import appdirs
import base64
import flask
import json
import os
import secrets
import time

from dash_spa.logging import log


def _session_keys(directory):

    # https://github.com/T4rk1n
    # https://github.com/plotly/dash-labs/blob/sessions/dash_labs/session/__init__.py

    key = os.getenv("DASH_SESSION_KEY")
    salt = os.getenv("DASH_SESSION_SALT")

    if not key or not salt:
        keyfile = os.path.join(directory, "keys.json")

        if os.path.exists(keyfile):
            with open(keyfile) as f:
                data = json.load(f)

            return data["key"], data["salt"]

        log.warn("Keys for session system are generated randomly and stored locally!")

        key = secrets.token_hex(128)
        salt = secrets.token_hex(128)

        os.makedirs(directory, exist_ok=True)
        with open(keyfile, "w") as f:
            json.dump({"key": key, "salt": salt}, f)

    return key, salt


def setup_sessions(
    app,
    session_cookie="_dash_spa_sessionid",
    max_age=84600 * 31,
    refresh_after=84600 * 7):

    # https://github.com/T4rk1n
    # https://github.com/plotly/dash-labs/blob/sessions/dash_labs/session/__init__.py

    key, salt = _session_keys(appdirs.user_config_dir("dash_spa"))

    signer = Signer(key, salt=salt)

    @app.server.before_request
    def session_middleware():

        token = flask.request.cookies.get(session_cookie)

        def set_session(_id):
            ts = base64.b64encode(str(int(time.time())).encode()).decode()

            @flask.after_this_request
            def _set_session(response):
                response.set_cookie(
                    session_cookie,
                    signer.sign(f"{_id}#{ts}").decode(),
                    httponly=True,
                    max_age=max_age,
                    samesite="Strict",
                )
                return response

        def new_session():
            sid = secrets.token_hex(32)
            set_session(sid)
            return sid

        if not token:
            session_id = new_session()
        else:
            try:
                unsigned = signer.unsign(token).decode()
                session_id, created = unsigned.split("#")

                delta = time.time() - int(base64.b64decode(created))
                if delta > refresh_after:
                    set_session(session_id)
            except BadSignature:
                session_id = new_session()

        flask.g.session_id = session_id
