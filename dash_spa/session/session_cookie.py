from flask import session, current_app as app
from ..spa_pages import DashSPA
from werkzeug.local import LocalProxy
from itsdangerous import Signer
import appdirs

import threading
import json
import os
import secrets


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
        log.info('Create SessionCookieManager()')

        self.refresh_after = refresh_after
        self.max_age = max_age

        # https://github.com/T4rk1n
        # https://github.com/plotly/dash-labs/blob/sessions/dash_labs/session/__init__.py

        key, salt = _session_keys(appdirs.user_config_dir("dash_spa"))
        self.signer = Signer(key, salt=salt)

        self.unattached_session_id = None


    @synchronized(SESSION_LOCK)
    def attach_session(self, response):
        """ Save unattached session id to cookie

        Must be called by @app.server.after_request
        """

        if self.unattached_session_id:
            log.info('Response, attach session id=%s', self.unattached_session_id)
            session[SPA_SESSION_COOKIE] = self.unattached_session_id
            self.unattached_session_id = None

    def create_session_id(self):
        sid = secrets.token_hex(32)
        log.info('create_unattached_session=%s', sid)
        return sid

    @synchronized(SESSION_LOCK)
    def get_session_id(self) -> str:
        """Return the session_id for the current session"""

        if self.unattached_session_id:
            return self.unattached_session_id

        # Extract the session from the current request cookies. If
        # this fails we create a new session_id and flag it as being
        # unattached_. The unattached session_id is

        try:

            if not SPA_SESSION_COOKIE in session:
                session[SPA_SESSION_COOKIE] = self.create_session_id()

            log.info('Using attached session id=%s', session[SPA_SESSION_COOKIE])
            return session[SPA_SESSION_COOKIE]

        except Exception:
            self.unattached_session_id = self.create_session_id()
            log.info('Using unattached session id=%s', self.unattached_session_id)

            try:
                @app.after_request
                def res_session_id(response):
                    self.attach_session(response)
                    return response
            except Exception:
                pass

            return self.unattached_session_id

def _sessionCookieManager():

    if not hasattr(_sessionCookieManager,'time'):
        _sessionCookieManager.time = -1

    if DashSPA.start_time != _sessionCookieManager.time:
        _sessionCookieManager.time = DashSPA.start_time
        _sessionCookieManager.sessionCookieManager = SessionCookieManager()

    return _sessionCookieManager.sessionCookieManager


# session_manager = SessionCookieManager()

session_manager = LocalProxy(_sessionCookieManager)
