import dash
from dash import html
from dash_spa.logging import log
from dash_spa.spa_context import createContext, ContextState, dataclass

@dataclass
class ButtonState(ContextState):
    clicks: int = 0

ButtonContext = createContext(ButtonState);

def Button():
    btn = html.Button("Button", id='btn')

    @ButtonContext.On(btn.input.n_clicks, prevent_initial_call=True)
    def btn_click(clicks):
        state = ButtonContext.getState()
        log.info('btn_click clicks=%s, state=%s', clicks, state)
        state.clicks += 1

    return btn

def test_button(dash_duo):
    app = dash.Dash(__name__)

    btn = None
    container = None

    @ButtonContext.Provider(id='test')
    def layout():
        nonlocal btn, container
        state = ButtonContext.getState()
        log.info('layout state=%s', state)
        btn = Button()
        container = html.Div(f"Button pressed {state.clicks} times!", id='container')
        return html.Div([btn, container])

    app.layout = layout()
    dash_duo.start_server(app)

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(container.css_id, text, timeout=4)

    assert wait_text("Button pressed 0 times!")

    _container = dash_duo.find_element(container.css_id)
    _btn = dash_duo.find_element(btn.css_id)

    assert _container.text == 'Button pressed 0 times!'

    _btn.click()
    assert wait_text("Button pressed 1 times!")

    _btn.click()
    assert wait_text("Button pressed 2 times!")

    _btn.click()
    assert wait_text("Button pressed 3 times!")

    _btn.click()
    assert wait_text("Button pressed 4 times!")
