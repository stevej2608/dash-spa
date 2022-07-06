from dash import dcc, html, clientside_callback
from dash_spa import prefix, copy_factory

# Note: requires sweetalert2 library. Make sure the following is included
# in the dash app instantiation:
#
# external_scripts = [
#     "https://cdn.jsdelivr.net/npm/sweetalert2@11.4.20/dist/sweetalert2.all.min.js"
#     ]
#
# app = dash.Dash( __name__,
#     external_scripts=external_scripts
#     )
#

class SweetAlert(html.Div):

    def __init__(self, id, title, text, icon=None, footer=None, show_confirm_button=False, timer=None):
        pid = prefix(id)

        swal2 = {}

        if title:
            swal2['title'] = title

        if text:
            swal2['text'] = text

        if icon:
            swal2['icon'] = icon

        if footer:
            swal2['footer'] = footer

        if show_confirm_button:
            swal2['showConfirmButton'] = show_confirm_button

        if timer:
            swal2['timer'] = timer


        store = dcc.Store(id=pid('store'), data=swal2, storage_type='memory')
        dummy = html.Div(id=pid('dummy'))


        clientside_callback(
            """
            function(timestamp, data) {

                console.log('SweetAlert.clientside_callback %s', data)

                const swalWithBootstrapButtons = Swal.mixin({
                    customClass: {
                        confirmButton: 'btn btn-primary',
                        cancelButton: 'btn btn-gray'
                    },
                    buttonsStyling: false
                });

                swalWithBootstrapButtons.fire(data)

                return data

            }
            """,
            dummy.output.children,
            store.input.modified_timestamp,
            store.state.data,
            prevent_initial_call=True
        )

        super().__init__([store, dummy])
        copy_factory(store, self)
