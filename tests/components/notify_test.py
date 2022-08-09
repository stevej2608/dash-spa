import dash
from dash import html
from dash_spa.logging import log
from dash_spa import spa_pages, NOUPDATE, page_container, register_page

from dash_spa.components.notyf import Notyf, SPA_NOTIFY
from dash_spa.utils.dumps_layout import dumps_layout

def single_page_app(page_layout):
    log.info('********************* create notify app ************************')
    app = dash.Dash(__name__,  plugins=[spa_pages])
    register_page(path='/', title="test", layout=page_layout())
    app.layout = page_container
    return app

def test_notify(dash_duo):

    # Create Dash UI and start the test server

    btn = None

    def layout():
        nonlocal btn

        btn = html.Button("Button", id='btn')

        @SPA_NOTIFY.update(btn.input.n_clicks)
        def btn_cb(clicks, store):
            if clicks:
                log.info('Notify click')
                notyf = Notyf(message='TESTING NOTIFY TESTING')
                return notyf.report()
            else:
                return NOUPDATE

        return html.Div([btn])

    app = single_page_app(layout)
    dash_duo.start_server(app)

    layout = dumps_layout(app.layout)
    assert layout == {
            "props": {
                "children": [
                {
                    "props": {
                    "id": "_pages_plugin_location"
                    },
                    "type": "Location",
                    "namespace": "dash_core_components"
                },
                {
                    "props": {
                    "children": [],
                    "id": "_pages_plugin_content"
                    },
                    "type": "Div",
                    "namespace": "dash_html_components"
                },
                {
                    "props": {
                    "id": "_pages_plugin_store"
                    },
                    "type": "Store",
                    "namespace": "dash_core_components"
                },
                {
                    "props": {
                    "children": [],
                    "id": "_pages_plugin_dummy"
                    },
                    "type": "Div",
                    "namespace": "dash_html_components"
                },
                {
                    "props": {
                    "children": [
                        {
                        "props": {
                            "id": "spa_location_store",
                            "data": [],
                            "storage_type": "session"
                        },
                        "type": "Store",
                        "namespace": "dash_core_components"
                        }
                    ],
                    "id": "spa_location_store#container"
                    },
                    "type": "Div",
                    "namespace": "dash_html_components"
                },
                {
                    "props": {
                    "id": "spa_location",
                    "refresh": False
                    },
                    "type": "Location",
                    "namespace": "dash_holoniq_components"
                },
                {
                    "props": {
                    "children": [
                        {
                        "props": {
                            "id": "spa_notify",
                            "data": {},
                            "storage_type": "memory"
                        },
                        "type": "Store",
                        "namespace": "dash_core_components"
                        },
                        {
                        "props": {
                            "id": {
                            "type": "spa_notify_ip",
                            "idx": "PYTEST_REPLACEMENT_ID_0"
                            },
                            "data": {},
                            "storage_type": "memory"
                        },
                        "type": "Store",
                        "namespace": "dash_core_components"
                        }
                    ],
                    "id": "spa_notify#container"
                    },
                    "type": "Div",
                    "namespace": "dash_html_components"
                }
                ]
            },
            "type": "Div",
            "namespace": "dash_html_components"
            }


    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal(".notyf__message", "TESTING NOTIFY TESTING", timeout=3)
    assert result
