from dataclasses import _process_class
from dash_spa.context_state import ContextState
from dash_spa.utils.caller import caller_hash
from dash_spa.logging import log
from .backends.backend_factory import SessionBackendFactory
from .session_cookie import session_manager


"""Minimalistic Server side session storage plugin

Usage:
```
from dash_spa import session_context, session_data


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


def session_data(cls=None, init=True, repr=True, eq=True,
                 order=False, unsafe_hash=False, frozen=False, id=None):
    """Wrapper for @dataclass, same functionality with addition of id

    TODO: Define cache expiry argument

    Args:
        id (str, optional): id of session data. Defaults to hash derived from module.line_number.
    """

    if id == None:
        id = caller_hash()

    def _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id=None):

        setattr(cls, '__session_data_id__', id)
        cls = _process_class(cls, init, repr, eq, order, unsafe_hash, frozen)
        return cls

    def wrap(cls):
        return _process_session_class(cls, init, repr, eq, order, unsafe_hash, frozen, id)

    if cls is None:
        return wrap

    return wrap(cls)

def session_context(session_ctx: SessionContext, id=None):
    """Get the context for the given SessionContext template

    Args:
        ctx (ContextState): The context data template to be returned
        id (str, optional): id of session data instance. Defaults to None.

    Returns:
        SessionContext: The current context state
    """

    cache = SessionBackendFactory.get_cache()

    # If the context id is none fallback on the data id. This allows
    # the same (global) session data to be to be used anywhere
    # in the application

    if id is None:
        id = session_ctx.__session_data_id__

    data = cache.get(id)
    # log.info('read  cache[%s] %s', id, data)

    # Create the requested context and map the session store. Use
    # the context.update_listener() capability to force an update
    # if the server cache whenever a state value is updated

    def update(new_state):
        cache.set(id, new_state)

    # Listen for changes in the data and update
    # the store on change

    # TODO: Is update needed? maybe just writing session at end of request would
    #  work just as well. Investigate!

    state: SessionContext = session_ctx()
    state.update(state=data, update_listener=update)

    return state


