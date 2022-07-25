import dash
from dash import html
from dash_spa import prefix, callback, NOUPDATE, session_context, session_data, SessionContext, spa_session, dash_logging
from dash_spa.logging import log

# Simple Dash App, single button when clicked increments session
# data clicks count. The test confirms that the session data is
# persistent and the latest state is presented for update in
# the button callback.

def test_session_button(dash_duo):
    pfx = prefix("session_test")
    BUTTON_TEST ='Button Test'

    # dash_duo.driver.delete_all_cookies()

    app = dash.Dash(__name__, plugins=[spa_session])


    @session_data(id='button_state')
    class ButtonState(SessionContext):
        clicks: int = 0

    # Layout the test app

    btn = html.Button("Button", id=pfx('session_btn'))
    container = html.Div(BUTTON_TEST, id=pfx('container'))

    @callback(container.output.children, btn.input.n_clicks, prevent_initial_call=True)
    def btn1_update(clicks):
        ctx = session_context(ButtonState)
        log.info('btn1_update clicks=%s', ctx.clicks)
        if clicks:
            ctx.clicks += 1
            return f"Button pressed {ctx.clicks} times!"
        return NOUPDATE

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(container.css_id, text, timeout=4)

    # Start the server

    app.layout = html.Div([btn, container])
    dash_duo.start_server(app)

    # Get button reference

    _btn = dash_duo.find_element(btn.css_id)

    # Testing

    assert wait_text(BUTTON_TEST)

    _btn.click()
    assert wait_text("Button pressed 1 times!")

    _btn.click()
    assert wait_text("Button pressed 2 times!")

    _btn.click()
    assert wait_text("Button pressed 3 times!")

    _btn.click()
    assert wait_text("Button pressed 4 times!")
