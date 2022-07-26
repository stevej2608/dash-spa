import uuid
import json
from dataclasses import _process_class
from diskcache import Cache
from flask import request
from dash_spa.logging import log
from dash_spa.spa_config import config
from dash_spa.utils.json_coder import json_decode, json_encode


options = config.get('session_storage')

SPA_SESSION_ID = "spa_session"

def plug(app):

    @app.server.after_request
    def res_session_id(response):
        req = request
        if hasattr(req,'sid') and req.sid is not None:
            log.info('Save session cookie id=%s', req.sid)
            response.set_cookie(SPA_SESSION_ID, req.sid)
            req.sid = None
        return response


class ServerSessionCache:
    """Wrapper for an individual session

    A single json string, indexed on session_id, is held in
    the server-side session cache. The cache should be thread and
    multi-process safe since each session has a uniq uuid and all the
    session data is stored in a single key.

    Use get(key) to get the value of an individual element in session dict.

    Use update() to save the entire session data dict

    Use clear() to remove all session entries from the cache

    """

    # TODO: Figure out how to test if this is thread & process safe

    _disk_cache =  Cache(directory = f"{options.folder}/spa_session")

    expiry = options.get('days', 30) * 24 * 60 * 60

    def __init__(self):

        try:
            req = request

            # Get the session id from the client cookies. If this
            # is the first request the cookie will not have been set
            # yet.

            if SPA_SESSION_ID in req.cookies:
                self.session_id = req.cookies[SPA_SESSION_ID]
            else:

                # Create an unattached session.This will be turned into
                # an attached session when the cookie is set. See:
                # @app.server.after_request

                self.session_id = str(uuid.uuid4())
                req.sid = self.session_id

        except Exception:
            log.info('No request object - using a dummy session store')
            self.session_id = "aaaaaaaa-bbbb-cccc-dddd-000000000000"


        if self.session_id in ServerSessionCache._disk_cache:
            json_str = ServerSessionCache._disk_cache[self.session_id]
            self.session_store = json.loads(json_str, object_hook=json_decode)
        else:
            log.info("Create new session store id=%s", self.session_id)
            self.session_store = {}

    def update(self):
        # log.info('write cache[%s]=%s', self.session_id, self.session_store)
        json_str = json.dumps(self.session_store, default=json_encode)
        ServerSessionCache._disk_cache.set(self.session_id, json_str, self.expiry)


    def get(self, obj_key) -> dict:
        if not obj_key in self.session_store:
            self.session_store[obj_key] = {}
        return self.session_store[obj_key]


    def put(self, obj_key, value: dict):
        self.session_store[obj_key] = value
        self.update()


    @staticmethod
    def clear():
        """Remove all items from cache.

        Removing items is an iterative process. In each iteration, a subset of
        items is removed. Concurrent writes may occur between iterations.
        """
        ServerSessionCache._disk_cache.clear()

