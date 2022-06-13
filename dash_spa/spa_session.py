import uuid
from dataclasses import dataclass
from flask import  session
from .logging import log
from .context_state import ContextState

SPA_SESSION_ID = "spa_session_id"


@dataclass
class SessionContext(ContextState):
    _context_id = str(uuid.uuid4())

# TODO: Make this thread safe

session_store = {}

def session_context(ctx: ContextState):
    try:
        sid = session[SPA_SESSION_ID]

        # Get the session store, create it if needed

        if not sid in session_store:
            session_store[sid] = {}

        store = session_store[sid]

        # Get the ctx context store, create it if needed

        if not ctx._context_id in store:
            store[ctx._context_id] = {}

        store = store[ctx._context_id]

    except Exception:
        store = {}

    state = ctx()
    state.map_store(store=store)
    return state


def session_contextX(ctx: ContextState):
    try:
        id = f"spa_{ctx.id}"
        if not id in session:
            session[id] = {}

        log.info('SESSION %s', session)

        store = session[id]
    except Exception:
        store = {}

    state = ctx()
    state.map_store(store=store)
    return state
