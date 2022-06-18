import uuid
from diskcache import Cache
import zlib
import json
from dataclasses import dataclass
from flask import request
from ..logging import log
from ..spa_config import config
from ..context_state import ContextState

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
from dash_spa import session_context, SessionContext, dataclass


@dataclass
class TickerState(SessionContext):
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

@dataclass
class SessionContext(ContextState):
    """Base class from which all contexts should be derived"""

    @staticmethod
    def id():
        return str(uuid.uuid4())

def plug(app):

    sid = None

    @app.server.before_request
    def req_session_id():
        global sid
        try:
            req = request
            if not SPA_SESSION_ID in req.cookies:
                sid = str(uuid.uuid4())
                log.info('Created session id=%s', sid)
        except Exception:
            pass

    @app.server.after_request
    def res_session_id(response):
        global sid
        if sid is not None:
            log.info('Save session cookie id=%s', sid)
            response.set_cookie(SPA_SESSION_ID, sid)
            sid = None
        return response

def session_context(ctx: SessionContext):
    """Get the context for the given SessionContext template. Create it if
    none exists

    Args:
        ctx (ContextState): The context template to be returned

    Returns:
        SessionContext: The current context state
    """

    req = request
    sid = req.cookies[SPA_SESSION_ID]

    try:
        cache = ServerSessionCache(sid)

        # Get the ctx context store for this session, create it if needed

        store = cache.get_json(ctx._context_id)
        log.info('read  cache[%s] %s', ctx._context_id, store)

        # Add an update listener

        enable_cache_update = False

        def update_listener():
            if enable_cache_update:
                log.info('write cache[%s] %s', ctx._context_id, store)
                cache.put_json(ctx._context_id, store)

        store = NotifyDict(update_listener, **store)

        # Create the requested context and map the session store

        state = ctx()
        state.map_store(store=store)

        # Writes to the context will update the session cache from here
        # onwards

        enable_cache_update = True
        return state

    except Exception:
        log.warn('Using a dummy session store id=%s', sid)
        store = {}
        state = ctx()
        state.map_store(store=store)
        return state
