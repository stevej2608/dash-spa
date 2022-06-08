from flask import current_app as app
from dash import callback as dash_callback
from .logging import log


def callback(*_args, **_kwargs):
    def callback_stub(*_args, **_kwargs):
        pass

    if app and app.got_first_request:
        log.info('Dismiss @callback decorator - server has started')
        return callback_stub
    else:
        return dash_callback(*_args, **_kwargs)
