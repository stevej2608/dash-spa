from flask import current_app as app
from werkzeug.local import LocalProxy
from dash_redux import ReduxStore
from dash import clientside_callback
from dash._callback import GLOBAL_CALLBACK_MAP
from dash_spa import page_container_append, add_external_scripts, add_external_stylesheets, current_app
from dash_spa.logging import log

"""Support for Notifications


Usage:
    @SPA_NOTIFY.update(btn3.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='This might be dangerous.', type='warning')
            return notyf.report()
        else:
            return NOUPDATE

See: https://github.com/caroso1222/notyf#readme
"""

class Notyf:

    Default = {
        'position': {
            'x': 'left',
            'y': 'top',
        },
        'types': [
            {
                'type': 'info',
                'background': '#0948B3',
                'icon': {
                    'className': 'fas fa-info-circle',
                    'tagName': 'span',
                    'color': '#fff'
                },
                'dismissible': False
            }
        ]
    }

    Error = {
        'position': {
            'x': 'right',
            'y': 'top',
        },
        'types': [
            {
                'type': 'error',
                'background': '#FA5252',
                'icon': {
                    'className': 'fas fa-times',
                    'tagName': 'span',
                    'color': '#fff'
                },
                'dismissible': False
            }
        ]
    }

    Warning = {
        'position': {
            'x': 'left',
            'y': 'bottom',
        },
        'types': [
            {
                'type': 'warning',
                'background': '#F5B759',
                'icon': {
                    'className': 'fas fa-exclamation-triangle',
                    'tagName': 'span',
                    'color': '#fff'
                },
                'dismissible': False
            }
        ]
    }

    Info = {
                'position': {
                    'x': 'right',
                    'y': 'bottom',
                },
                'types': [
                    {
                        'type': 'info',
                        'background': '#262B40',
                        'icon': {
                            'className': 'fas fa-comment-dots',
                            'tagName': 'span',
                            'color': '#fff'
                        },
                        'dismissible': False
                    }
                ]
            }

    def __init__(self, message, type=None, template=None):

        if template == None:
            if type == 'error':
                template = Notyf.Error
            elif type == 'warning':
                template = Notyf.Warning
            elif type == 'info':
                template = Notyf.Info
            else:
                type = 'info'
                template = Notyf.Default

        self.notyf = {}
        self.notyf.update(template)

        self.notyf['_message'] = message
        self.notyf['_type'] = type

    def report(self):
        return self.notyf

class NotyfViewer(ReduxStore):

    def __init__(self, id):

        add_external_scripts("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.js")
        add_external_stylesheets("https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.css")

        super().__init__(id=id, storage_type='memory', data={})

        clientside_callback(
            """
            function(data) {

                const {_message, _type, ...template} = data
                const notyf = new Notyf(template);

                notyf.open({
                    type: _type,
                    message: _message
                });

            }
            """,
            self.store.output.modified_timestamp,
            self.store.input.data,
            prevent_initial_call=True
        )


    def update(self, *_args, **_kwargs):

        def callback_stub(self, *_args, **_kwargs):
            pass

        if app and app.got_first_request:
            return callback_stub

        return super().update(*_args, **_kwargs)

# The GLOBAL_CALLBACK_MAP is cleared when Dash sends the initial
# app layout to the browser. A problem occurs when testing. The
# initial test setup will send the SPA_NOTIFY component and associated
# client callback and the test will pass. Any subsequent will fail
# because the GLOBAL_CALLBACK_MAP is empty.

# The following LocalProxy fixes the problem.

def _notyfViewer():

    if not current_app:
        return None

    if 'spa_notify.data' not in GLOBAL_CALLBACK_MAP:
        # log.info('Create NotyfViewer instance')
        _notyfViewer.viewer = NotyfViewer(id='spa_notify')
        page_container_append(_notyfViewer.viewer)

    return _notyfViewer.viewer


SPA_NOTIFY = LocalProxy(_notyfViewer)
"""Spa Notify callback wrapper

Usage:
    @SPA_NOTIFY.update(btn3.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='This might be dangerous.', type='warning')
            return notyf.report()
        else:
            return NOUPDATE
"""
