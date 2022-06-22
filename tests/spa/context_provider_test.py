import dash
from dash import html
from dash_spa.logging import log
from dash_spa.spa_context import createContext, ContextState, dataclass

@dataclass
class ButtonState(ContextState):
    clicks: int = 0

ButtonContext = createContext(ButtonState);

# Define button with associated callback. Button context is incremented
# on each click

def Button():
    btn = html.Button("Button", id='btn')

    @ButtonContext.On(btn.input.n_clicks, prevent_initial_call=True)
    def btn_click(clicks):
        state = ButtonContext.getState()
        state.clicks += 1

    return btn

def test_button(dash_duo):
    app = dash.Dash(__name__)

    btn = None
    container = None

    # Dash layout() decorated with Context.Provider. This will be called
    # every time the ButtonContext changes

    @ButtonContext.Provider(id='test')
    def layout():
        nonlocal btn, container
        state = ButtonContext.getState()
        log.info('layout state=%s', state)
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
    assert wait_text("Button pressed 0 times!")

    _btn.click()
    assert wait_text("Button pressed 1 times!")

    _btn.click()
    assert wait_text("Button pressed 2 times!")

    _btn.click()
    assert wait_text("Button pressed 3 times!")

    _btn.click()
    assert wait_text("Button pressed 4 times!")
