import dash
from dash import html
from dash_spa.logging import log
from dash_spa import DashSPA, NOUPDATE, page_container, register_page

from dash_spa.components import Notyf, SPA_NOTIFY
from dash_spa.utils.dumps_layout import dumps_layout

def single_page_app(page_layout):
    log.info('********************* create notify app ************************')
    app = DashSPA(__name__, pages_folder='')
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

    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal(".notyf__message", "TESTING NOTIFY TESTING", timeout=3)
    assert result
