import uuid
from dataclasses import dataclass, _process_class
from diskcache import Cache
import zlib
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

class ServerSessionCache:

    COMPRESS_LEVEL = 6

    sessions = {}

    def __init__(self, sid, days=0, hours=0, minutes=0, seconds=0, compress_level = COMPRESS_LEVEL):
        if sid in ServerSessionCache.sessions:
            self.cache = self.sessions[sid]
        else:
            self.cache = Cache(f"{options.folder}/spa_session_{sid}")
            self.sessions[sid] = self.cache

        if days == 0 and options.get('days', None) is not None:
            days = options.days

        if (days == 0 and hours == 0 and minutes == 0 ):
            minutes = 15

        self.expiry = (((days * 24 + hours) * 60 + minutes) * 60) + seconds

        self.compress_level = compress_level


    def get_json(self, key):
        if key in self.cache:
            json_str = zlib.decompress(self.cache[key]).decode()
            return json.loads(json_str, object_hook=json_decode)
        else:
            return {}

    def put_json(self, key, obj):
        json_str = json.dumps(obj, default=json_encode)
        data = zlib.compress(json_str.encode(), self.compress_level)
        self.cache.set(key, data, self.expiry)


    def delete_page(self, key):
        self.cache.delete(key)

    def clear_cache(self):
        self.cache.clear()

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

class SessionContext(ContextState):
    pass

def session_context(ctx: SessionContext):
    """Get the context for the given SessionContext template. Create it if
    none exists

    Args:
        ctx (ContextState): The context template to be returned

    Returns:
        SessionContext: The current context state
    """

    req = request

    try:

        # Get the session id from the client cookies. If this
        # is the first request the cookie will not have been set
        # yes but it is available on the request object

        if SPA_SESSION_ID in req.cookies:
            sid = req.cookies[SPA_SESSION_ID]
        elif hasattr(req,'sid') and req.sid is not None:
            sid = req.sid

        cache = ServerSessionCache(sid)

        # Get the ctx context store for this session, create it if needed

        store = cache.get_json(ctx.__session_data_id__)
        log.info('read  cache[%s] %s', ctx.__session_data_id__, store)

        # Add an update listener

        enable_cache_update = False

        def update_listener():
            if enable_cache_update:
                log.info('write cache[%s] %s', ctx.__session_data_id__, store)
                cache.put_json(ctx.__session_data_id__, store)

        store = NotifyDict(update_listener, **store)

        # Create the requested context and map the session store

        state = ctx()
        state.set_shadow_store(store=store)

        # Writes to the context will update the session cache from here
        # onwards

        enable_cache_update = True
        return state

    except Exception:
        log.warn('Using a dummy session store id=%s', sid)
        store = {}
        state = ctx()
        state.set_shadow_store(store=store)
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