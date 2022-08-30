from dash import html
from dash_spa.logging import log
from dash_spa import NOUPDATE

from dash_spa.components import Alert, SPA_ALERT
from .app_factory import single_page_app

class Page():

    def __init__(self):
        self.btn = html.Button("Alert Button", id='alert_btn')

    def layout(self):

        @SPA_ALERT.update(self.btn.input.n_clicks)
        def btn_cb(clicks, store):
            if clicks:
                log.info('issue alert')
                alert = Alert("Basic alert", 'You clicked the button!')
                return alert.report()
            else:
                return NOUPDATE

        return html.Div(self.btn)

def test_alert(dash_duo):

    page = Page()
    test_app = single_page_app(page.layout)
    dash_duo.start_server(test_app)

    # Click a button to trigger the notify toast

    browser_btn = dash_duo.find_element(page.btn.css_id)
    browser_btn.click()

    result = dash_duo.wait_for_text_to_equal("#swal2-title", "Basic alert", timeout=3)
    assert result

    result = dash_duo.wait_for_text_to_equal("#swal2-html-container", "You clicked the button!", timeout=3)
    assert result
