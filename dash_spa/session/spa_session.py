import uuid
from flask import request, current_app as app
from dataclasses import _process_class
from dash_spa.context_state import ContextState
from dash_spa.logging import log

from .backends.diskcache  import ServerSessionCache

SPA_SESSION_ID = "spa_session"

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


class SessionContext(ContextState):
    pass

def session_context(ctx: SessionContext, id=None):
    """Get the context for the given SessionContext template

    Args:
        ctx (ContextState): The context template to be returned

    Returns:
        SessionContext: The current context state
    """

    @app.after_request
    def res_session_id(response):
        req = request
        if hasattr(req,'sid') and req.sid is not None:
            log.info('Save session cookie id=%s', req.sid)
            response.set_cookie(SPA_SESSION_ID, req.sid)
            req.sid = None
        return response

    cache = ServerSessionCache()

    # Get the ctx context store for this session, create it if needed

    id = id if id is not None else ctx.__session_data_id__

    store = cache.get(id)
    # log.info('read  cache[%s] %s', id, store)

    # Create the requested context and map the session store. Use
    # the context.update_listener() capability to force an update
    # if the server cache whenever a state value is updated

    def update(new_state):
        cache.put(id, new_state)

    state = ctx()
    state.update(state=store, update_listener=update)

    return state


def session_data(cls=None, init=True, repr=True, eq=True,
                 order=False, unsafe_hash=False, frozen=False, id=None):
    """Wrapper for @dataclass, same functionality with addition of id

    TODO: Define cache expiry argument

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