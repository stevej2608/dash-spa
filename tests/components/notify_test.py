from dash import html
from dash_spa.logging import log
from dash_spa import NOUPDATE
from dash_spa.components import Notyf, SPA_NOTIFY

from .app_factory import single_page_app


class Page():

    def __init__(self):
        self.btn = html.Button("Button", id='btn')

    def layout(self):

        @SPA_NOTIFY.update(self.btn.input.n_clicks)
        def btn_cb(clicks, store):
            if clicks:
                log.info('Notify click')
                notyf = Notyf(message='TESTING NOTIFY TESTING')
                return notyf.report()
            else:
                return NOUPDATE

        return html.Div(self.btn)

def test_notify(dash_duo):

    page = Page()
    test_app = single_page_app(page.layout)
    dash_duo.start_server(test_app)

    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(page.btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal(".notyf__message", "TESTING NOTIFY TESTING", timeout=3)
    assert result
