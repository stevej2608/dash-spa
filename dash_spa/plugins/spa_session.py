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

    @app.server.before_first_request
    @app.server.before_request
    def req_session_id():
        try:
            req = request
            if not SPA_SESSION_ID in req.cookies:
                req.sid = str(uuid.uuid4())
        except Exception:
            pass

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
    the server-side session cache.

    Use get(key) to get the value of an individual element in session dict.

    Use update() to save the entire session data dict



    """

    disk_cache =  Cache(directory = f"{options.folder}/spa_session")
    mem_cache = {}

    expiry = options.get('days', 30) * 24 * 60 * 60

    def __init__(self):

        try:
            req = request

            # Get the session id from the client cookies. If this
            # is the first request the cookie will not have been set
            # yes but it is available on the request object

            if SPA_SESSION_ID in req.cookies:
                self.session_id = req.cookies[SPA_SESSION_ID]
            else:
                self.session_id = req.sid

        except Exception:
            log.warn('Using a dummy session store')
            self.session_id = "dummy"

        if self.session_id in ServerSessionCache.mem_cache:
            return

        if self.session_id in ServerSessionCache.disk_cache:
            json_str = ServerSessionCache.disk_cache[self.session_id]
            store = json.loads(json_str, object_hook=json_decode)
        else:
            log.info("Create new session store id=%s", self.session_id)
            store = {}

        ServerSessionCache.mem_cache[self.session_id] = store

    def update(self):
        session_store = ServerSessionCache.mem_cache[self.session_id]
        log.info('write cache[%s]=%s', self.session_id, session_store)
        json_str = json.dumps(session_store, default=json_encode)
        ServerSessionCache.disk_cache.set(self.session_id, json_str, self.expiry)

    def get(self, obj_key) -> dict:
        session_store = ServerSessionCache.mem_cache[self.session_id]
        if not obj_key in session_store:
            session_store[obj_key] = {}
        return session_store[obj_key]

    def put(self, obj_key, value):
        session_store = ServerSessionCache.mem_cache[self.session_id]

        if not obj_key in session_store:
            session_store[obj_key] = {}

        store = session_store[obj_key]
        store.update(value)
        self.update()


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