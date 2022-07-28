from flask import request
from itsdangerous import Signer, BadSignature
import appdirs
import base64
import threading
import json
import os
import secrets
import time

from dash_spa.spa_config import config
from dash_spa.logging import log
from  dash_spa.utils import synchronized

options = config.get('session_storage')

SPA_SESSION_COOKIE = options.get("session_cookie", "_dash_spa_sessionid")

SESSION_LOCK = threading.Lock()

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

class SessionCookieManager:

    def __init__(self, max_age=84600 * 31,refresh_after=84600 * 7):
        self.refresh_after = refresh_after
        self.max_age = max_age

        # https://github.com/T4rk1n
        # https://github.com/plotly/dash-labs/blob/sessions/dash_labs/session/__init__.py

        key, salt = _session_keys(appdirs.user_config_dir("dash_spa"))
        self.signer = Signer(key, salt=salt)

        self.session_id = None
        self.unattached_session_id = False


    @synchronized(SESSION_LOCK)
    def attach_session(self, response):
        """ Save unattached session id to cookie

        Must be called by @app.server.after_request
        """

        if self.unattached_session_id:
            log.info('Response, attach session id=%s', self.session_id)

            ts = base64.b64encode(str(int(time.time())).encode()).decode()

            response.set_cookie(
                SPA_SESSION_COOKIE,
                self.signer.sign(f"{self.session_id}#{ts}").decode(),
                httponly=True,
                max_age=self.max_age,
                samesite="Strict"
            )

            self.session_id = None
            self.unattached_session_id = False

    def create_unattached_session(self):
        sid = secrets.token_hex(32)
        self.unattached_session_id = True
        return sid

    @synchronized(SESSION_LOCK)
    def get_session_id(self) -> str:
        """Return the session_id for the current session"""

        if self.session_id:
            return self.session_id

        # Extract the session from the current request cookies. If
        # this fails we create a new session_id and flag it as being
        # unattached_. The unattached session_id is

        try:
            req = request
            self.unattached_session_id = False

            # Get the session id from the client cookies. If this
            # is the first request the cookie will not have been set
            # yet.

            if SPA_SESSION_COOKIE in req.cookies:
                token = req.cookies.get(SPA_SESSION_COOKIE)
                try:
                    unsigned = self.signer.unsign(token).decode()
                    self.session_id, created = unsigned.split("#")

                    delta = time.time() - int(base64.b64decode(created))
                    if delta > self.refresh_after:
                        self.attach_session(self.session_id)

                except BadSignature:
                    self.session_id = self.create_unattached_session()
            else:

                # Create an unattached session.This will be turned into
                # an attached session when the cookie is set. See:
                # @app.server.after_request

                self.session_id = self.create_unattached_session()

        except Exception:
            self.session_id = self.create_unattached_session()

        log.info('get_session_id=%s', self.session_id)

        return self.session_id

session_manager = SessionCookieManager()
