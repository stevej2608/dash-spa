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
    btn = html.Button("Button", state.pid('btn'))

    @ButtonContext.On(btn.input.n_clicks, prevent_initial_call=True)
    def btn_click(clicks):
        state.clicks += 1

    return btn

def test_button(dash_duo):
    app = dash.Dash(__name__)

    # Dash layout() decorated with Context.Provider. layout() will be called
    # every time the ButtonContext changes

    def widget_layout():

        # The context Provider calls the wrapped function, in this
        # case 'widget_layout()' whenever the context is updated

        class _Wrapper(html.Div):
            def __init__(self, button, container):
                self.container = container
                self.btn = button
                super().__init__([button, container])

        state = ButtonContext.getState()

        btn = Button()
        container = html.Div(f"Button pressed {state.clicks} times!", state.pid('container'))

        return _Wrapper(btn, container)


    # Create Dash UI and start the test server

    widget = ButtonContext.Provider(id='test_btn')(widget_layout)()
    app.layout = widget
    dash_duo.start_server(app)

    # Test code

    def wait_text(text):
        return dash_duo.wait_for_text_to_equal(widget.container.css_id, text, timeout=4)

    _btn = dash_duo.find_element(widget.btn.css_id)
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
