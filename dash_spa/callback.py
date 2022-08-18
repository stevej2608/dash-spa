# from flask import current_app as app
from dash import callback as dash_callback, get_app
from dash._callback import GLOBAL_CALLBACK_MAP
from .logging import log
from .utils.caller import caller_location


def callback(*_args, **_kwargs):
    """Wrapper for standard Dash callback decorator. Dismisses
    the callback and handler if the server is active. This does not mean the
    callback will not work, just that is does not need to be presented to
    the Dash subsystem again.
    """
    def callback_stub(*_args, **_kwargs):
        pass

    dash = get_app()

    # if app and app.got_first_request:
    #     log.info('Dismiss @callback decorator %s server has started', caller_location())
    #     return callback_stub

    if dash.is_live:
        # log.info('Dismiss @callback decorator %s server has started', caller_location())
        return callback_stub

    return dash_callback(*_args, **_kwargs)
