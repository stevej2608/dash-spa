import sys
from flask import current_app as app
from dash import callback as dash_callback
from .logging import log

_cb_initialised = {}


def callback_hash(*_args):

    def unpack(id):

        # Handle dict the keys used by MATCH

        if isinstance(id, dict):
            id = [ part for part in id.values() if isinstance(part, str)]
            return '_'.join(id)
        else:
            return id


    # Create a positive hex hash all the callback inputs

    inputs = []
    for input in _args:
        id = f"{unpack(input.component_id)}.{input.component_property}"
        # log.info('input %s', id)
        inputs.append(id)
    _hash = hash(tuple(inputs))
    _hash += sys.maxsize + 1
    return hex(_hash)[2:]




def callback(*_args, **_kwargs):
    """Wrapper for standard Dash callback decorator. Dismisses
    the callback and handler if the server is active. This does not mean the
    callback will not work, just that is does not need to be presented to
    the Dash subsystem again.
    """
    def callback_stub(*_args, **_kwargs):
        pass

    cb_hash = callback_hash(*_args)

    if cb_hash in _cb_initialised:
        # log.info('Dismiss @callback decorator - server has started')
        return callback_stub
    else:
        _cb_initialised[cb_hash] = True
        return dash_callback(*_args, **_kwargs)
