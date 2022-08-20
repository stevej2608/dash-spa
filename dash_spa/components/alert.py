"""Support for Alerts

Usage:

```
    btn1 = html.Button("Basic alert", className='btn btn-gray-800', id='basicAlert1')
    @SPA_ALERT.update(btn1.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert("Basic alert", f'You clicked the button {clicks} times!')
            return alert.report()
        else:
            return NOUPDATE
```

Note: requires sweetalert2 library. Make sure the following is included
in the dash app instantiation:

```
external_scripts = [
    "https://cdn.jsdelivr.net/npm/sweetalert2@11.4.20/dist/sweetalert2.all.min.js"
    ]

app = dash.Dash( __name__,
    external_scripts=external_scripts
    )
```
"""

from flask import current_app as app
from werkzeug.local import LocalProxy
from dataclasses import dataclass
from dash_redux import ReduxStore
from dash import clientside_callback
from dash_spa import page_container_append, add_external_scripts, current_app
from dash_spa.logging import log
from dash._callback import GLOBAL_CALLBACK_MAP


@dataclass
class Alert:
    title: str = None
    text: str = None
    icon: str = None
    footer: str = None
    showConfirmButton: bool = None
    timer: int = None

    def report(self):
        args = {k:v for k,v in vars(self).items() if v is not None}
        return args

class SweetAlert(ReduxStore):

    def __init__(self, id):
        super().__init__(id=id, storage_type='memory', data={})

        add_external_scripts("https://cdn.jsdelivr.net/npm/sweetalert2@11.4.20/dist/sweetalert2.all.min.js")

        clientside_callback(
            """
            function(data) {

                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-primary',
                        cancelButton: 'btn btn-gray'
                    },
                    buttonsStyling: false
                });

                swalWithBootstrapButtons.fire(data)

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
#
# The following LocalProxy fixes the problem

def _sweetAlert():

    if not current_app:
        return None

    if 'spa_alert.data' not in GLOBAL_CALLBACK_MAP:
        # log.info('Create Alert instance')
        _sweetAlert.viewer = SweetAlert(id='spa_alert')
        page_container_append(_sweetAlert.viewer)
    return _sweetAlert.viewer



SPA_ALERT = LocalProxy(_sweetAlert)
"""Spa Alert callback wrapper
Usage:
    @SPA_ALERT.update(btn5.input.n_clicks)
    def btn_cb(clicks, store):
        if clicks:
            alert = Alert('The Internet?', 'That thing is still around?', icon='question')
            return alert.report()
        else:
            return NOUPDATE
"""
