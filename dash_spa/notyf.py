from flask import current_app as app
from dash_redux import ReduxStore
from dash import clientside_callback
from dash_spa import page_container_append

"""Support for Notifications

Usage:
    @SPA_NOTIFY.update(btn3.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            notyf = Notyf(message='This might be dangerous.', type='warning')
            return notyf.report()
        else:
            return NOUPDATE


Note: requires notyf library. Make sure the following is included
in the dash app instantiation:

    from dash_spa.notyf import NOTIFY_CSS, NOTIFY_JS

    external_stylesheets = [
        NOTIFY_CSS,
        ]

    external_scripts = [
        NOTIFY_JS
        ]

    app = dash.Dash( __name__,
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets
        )
"""

NOTIFY_CSS = "https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.css"
NOTIFY_JS = "https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.js"

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


SPA_NOTIFY = NotyfViewer(id='spa_notify')
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



page_container_append(SPA_NOTIFY)