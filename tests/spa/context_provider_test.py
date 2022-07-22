import dash
import pytest
from dash import html
from dash_spa.logging import log
from dash_spa.spa_context import createContext, ContextState, dataclass

@dataclass
class ButtonState(ContextState):
    clicks: int = 1000

ButtonContext = createContext(ButtonState);

# Define button with associated context callback. Button context is incremented
# on each click. The context maintains the number of button clicks

def Button():
    state = ButtonContext.getState()
    btn = html.Button("Button", id='btn')

    @ButtonContext.On(btn.input.n_clicks, prevent_initial_call=True)
    def btn_click(clicks):
        state.clicks += 1

    return btn

def test_button(dash_duo):
    app = dash.Dash(__name__)

    # These are only defined here to allow test access

    btn = None
    container = None

    # Dash layout() decorated with Context.Provider. layout() will be called
    # every time the ButtonContext changes

    @ButtonContext.Provider(id='test_btn')
    def layout():
        nonlocal btn, container

        state = ButtonContext.getState()

        btn = Button()
        container = html.Div(f"Button pressed {state.clicks} times!", id='container')

        return html.Div([btn, container])

    # Create Dash UI and start the test server

    app.layout = layout()
    dash_duo.start_server(app)

    # Test code

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(container.css_id, text, timeout=4)

    _btn = dash_duo.find_element(btn.css_id)
    assert wait_text("Button pressed 1000 times!")

    _btn.click()
    assert wait_text("Button pressed 1001 times!")

    _btn.click()
    assert wait_text("Button pressed 1002 times!")

    _btn.click()
    assert wait_text("Button pressed 1003 times!")

    _btn.click()
    assert wait_text("Button pressed 1004 times!")


def test_no_context():

    # Try and use context outside of provider - exception expected

    with pytest.raises(Exception):
        Button()
