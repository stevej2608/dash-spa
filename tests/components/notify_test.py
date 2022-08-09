import dash
from dash import html
from selenium.webdriver.common.by import By
from dash_spa import spa_pages, NOUPDATE, page_container, register_page
from server import serve_app

from dash_spa.components.alert import Alert, SPA_ALERT
from dash_spa.components.notyf import Notyf, SPA_NOTIFY

def single_page_app(page_layout):
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
                notyf = Notyf(message='TESTING NOTIFY TESTING')
                return notyf.report()
            else:
                return NOUPDATE

        return html.Div([btn])

    app = single_page_app(layout)
    dash_duo.start_server(app)

    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal(".notyf__message", "TESTING NOTIFY TESTING", timeout=3)
    assert result
