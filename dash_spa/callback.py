from dash import callback as dash_callback
from .spa_current_app import current_app
from .logging import log


def callback(*_args, **_kwargs):
    """Wrapper for standard Dash callback decorator. Dismisses
    the callback and handler if the server is active. This does not mean the
    callback will not work, just that is does not need to be presented to
    the Dash subsystem again.
    """
    def callback_stub(*_args, **_kwargs):
        pass

    if current_app and current_app.is_live:
        # log.info('Dismiss @callback decorator %s server has started', caller_location())
        return callback_stub

    return dash_callback(*_args, **_kwargs)
