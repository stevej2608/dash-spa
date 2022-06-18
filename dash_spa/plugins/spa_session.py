import uuid
from dataclasses import dataclass
from flask import session
from ..logging import log
from ..context_state import ContextState

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

SPA_SESSION_ID = "spa_session"

@dataclass
class SessionContext(ContextState):
    """Base class from which all contexts should be derived"""

    _context_id = str(uuid.uuid4())

# TODO: Make this thread safe

session_store = {}

def plug(app):

    @app.server.before_request
    def set_session_id():
        try:
            if not SPA_SESSION_ID in session:
                session[SPA_SESSION_ID] = str(uuid.uuid4())
                log.info('Created session id=%s', session[SPA_SESSION_ID])
        except Exception:
            pass

def session_context(ctx: SessionContext):
    """Get the context for the given SessionContext template. Create it if
    none exists

    Args:
        ctx (ContextState): The context template to be returned

    Returns:
        SessionContext: The current context state
    """

    try:
        sid = session[SPA_SESSION_ID]

        # Get the server side session store, create one if needed

        if not sid in session_store:
            session_store[sid] = {}

        store = session_store[sid]

        # Get the ctx context store for this session, create it if needed

        if not ctx._context_id in store:
            store[ctx._context_id] = {}

        store = store[ctx._context_id]

    except Exception:
        store = {}

    state = ctx()
    state.map_store(store=store)
    return state
