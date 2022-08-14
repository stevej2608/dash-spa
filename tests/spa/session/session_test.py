import pytest
from dash import html
from dash_spa import DashSPA, prefix, callback, NOUPDATE
from dash_spa.session import session_data, SessionContext, session_context
from dash_spa.logging import log

# Simple Dash App, single button when clicked increments session
# data clicks count. The test confirms that the session data is
# persistent and the latest state is presented for update in
# the button callback

@pytest.fixture()
def app():
    pfx = prefix("session_test")

    # dash_duo.driver.delete_all_cookies()

    app = DashSPA(__name__, use_pages=False)
    app.server.config['SECRET_KEY'] = "A secret key"

    @session_data()
    class ButtonState(SessionContext):
        clicks: int = 0

    # Layout the test app

    app.BUTTON_TEST ='Button Test'
    app.btn = html.Button("Button", id=pfx('session_btn'))
    app.container = html.Div(app.BUTTON_TEST, id=pfx('container'))

    @callback(app.container.output.children, app.btn.input.n_clicks, prevent_initial_call=True)
    def btn_update(clicks):
        ctx = session_context(ButtonState)
        log.info('btn1_update clicks=%s', ctx.clicks)
        if clicks:
            ctx.clicks += 1
            return f"Button pressed {ctx.clicks} times!"
        return NOUPDATE

    app.layout = html.Div([app.btn, app.container])
    return app


def test_session_button(dash_duo, app):

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(app.container.css_id, text, timeout=4)

    dash_duo.start_server(app)

    # Get button reference

    btn = dash_duo.find_element(app.btn.css_id)

    # Testing

    assert wait_text(app.BUTTON_TEST)

    btn.click()
    assert wait_text("Button pressed 1 times!")

    btn.click()
    assert wait_text("Button pressed 2 times!")

    btn.click()
    assert wait_text("Button pressed 3 times!")

    btn.click()
    assert wait_text("Button pressed 4 times!")
