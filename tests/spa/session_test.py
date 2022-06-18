import dash
from dash import html
from dash_spa import prefix, callback, NOUPDATE, session_context, SessionContext, dataclass, spa_session


@dataclass
class ButtonState(SessionContext):
    _context_id = SessionContext.id()
    clicks: int = 0


def test_button(dash_duo):
    pfx = prefix("session_test")
    BUTTON_TEST ='Button Test'

    app = dash.Dash(__name__, plugins=[spa_session])

    btn = html.Button("Button", id=pfx('btn'))
    container = html.Div(BUTTON_TEST, id=pfx('container'))

    @callback(container.output.children, btn.input.n_clicks)
    def btn1_update(clicks):
        ctx = session_context(ButtonState)
        if clicks:
            ctx.clicks += 1
            return f"Button pressed {clicks} times! "
        return NOUPDATE

    app.layout = html.Div([btn, container])
    dash_duo.start_server(app)

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(container.css_id, text, timeout=4)

    dash_duo.wait_for_text_to_equal(container.css_id, BUTTON_TEST, timeout=4)

    _container = dash_duo.find_element(container.css_id)
    _btn = dash_duo.find_element(btn.css_id)

    assert _container.text == BUTTON_TEST


    _btn.click()
    assert wait_text("Button pressed 1 times!")

    _btn.click()
    assert wait_text("Button pressed 2 times!")

    _btn.click()
    assert wait_text("Button pressed 3 times!")
