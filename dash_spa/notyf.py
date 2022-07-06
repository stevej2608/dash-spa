from dash import dcc, html, clientside_callback
from dash_spa import prefix, copy_factory

# Note: requires notyf library. Make sure the following is included
# in the dash app instantiation:
#
# external_scripts = [
#     "https://cdn.jsdelivr.net/npm/notyf@3/notyf.min.css"
#     ]
#
# app = dash.Dash( __name__,
#     external_scripts=external_scripts
#     )
#

class Notyf(html.Div):

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


    def __init__(self, id, message, type=None, template=None):
        pid = prefix(id)

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

        notyf = {}
        notyf.update(template)

        notyf['_message'] = message
        notyf['_type'] = type

        store = dcc.Store(id=pid('store'), data=notyf, storage_type='memory')
        dummy = html.Div(id=pid('dummy'))


        clientside_callback(
            """
            function(timestamp, data) {

                console.log('Notyf.clientside_callback %s', data)

                const {_message, _type, ...template} = data

                const notyf = new Notyf(template);

                notyf.open({
                    type: _type,
                    message: _message
                });

                return ""

            }
            """,
            dummy.output.children,
            store.input.modified_timestamp,
            store.state.data,
            prevent_initial_call=True
        )

        super().__init__([store, dummy])
        copy_factory(store, self)
