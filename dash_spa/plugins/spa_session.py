import uuid
from dataclasses import dataclass, _process_class
from diskcache import Cache
import json
from flask import request
from ..logging import log
from ..spa_config import config
from ..context_state import ContextState, dataclass

from ..utils.notify_dict import NotifyDict
from ..utils.json_coder import json_decode, json_encode

"""Minimalistic Server side session storage plugin

This plugin must be added to the Dash initialisation before use

*app.py*
```
import dash_spa as spa

app = Dash(__name__,
        plugins=[spa.spa_session],
        ...
```

Usage:
```
from dash_spa import session_context, , session_data


@session_data(id='ticker_state')
class TickerState:
    tickers: str = ""


def layout(tickers = None):
    ctx = session_context(TickerState)
    ctx.tickers = tickers if tickers is not None else ['AAPL', 'COKE']
    ...
```
"""

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
        log.info('write cache[%s]=%s', self.session_id, self.session_store)
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


class SessionContext(ContextState):
    pass

def session_context(ctx: SessionContext):
    """Get the context for the given SessionContext template

    Args:
        ctx (ContextState): The context template to be returned

    Returns:
        SessionContext: The current context state
    """

    cache = ServerSessionCache()

    # Get the ctx context store for this session, create it if needed

    store = cache.get(ctx.__session_data_id__)
    log.info('read  cache[%s] %s', ctx.__session_data_id__, store)

    # Create the requested context and map the session store. Use
    # the context.update_listener() capability to force an update
    # if the server cache whenever a state value is updated

    state = ctx()
    state.set_shadow_store(store=store, update_listener=cache.update)

    return state


def session_data(cls=None, init=True, repr=True, eq=True,
                 order=False, unsafe_hash=False, frozen=False, id=None):
    """Wrapper for @dataclass, same functionality with addition of id

    Args:
        id (str, optional): _description_. Defaults to None.
    """


    def _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id=None):
        id = id if id else str(uuid.uuid4())
        setattr(cls, '__session_data_id__', id)
        cls = _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)
        return cls

    def wrap(cls):
        return _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id)

    if cls is None:
        return wrap

    return wrap(cls)