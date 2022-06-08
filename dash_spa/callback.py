from flask import current_app as app
from dash import callback as dash_callback
from .logging import log


def callback(*_args, **_kwargs):
    """Wrapper for standard Dash callback decorator. Dismisses
    the callback and handler if the server is active. This does not mean the
    callback will not work, just that is does not need to be presented to
    the Dash subsystem again.
    """
    def callback_stub(*_args, **_kwargs):
        pass

    if app and app.got_first_request:
        # log.info('Dismiss @callback decorator - server has started')
        return callback_stub
    else:
        return dash_callback(*_args, **_kwargs)
