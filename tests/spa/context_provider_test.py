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

def button_widget_layout():
    """
    Simple test fixture consisting of a button and a div that
    communicate via the active ButtonContext. When the button is clicked the
    div displays a message reporting the number of clicks.
    """

    # Hack to allow tests to easily reference the button & container

    class _TestWrapper(html.Div):
        def __init__(self, button, container):
            self.container = container
            self.btn = button
            super().__init__([button, container])

    state = ButtonContext.getState()

    btn = Button()
    container = html.Div(f"Button pressed {state.clicks} times!", state.pid('container'))

    return _TestWrapper(btn, container)


def test_no_context():

    # Try and use context outside of provider - exception expected

    with pytest.raises(Exception) as error:
        Button()

    assert "Context can only be used within the scope of a provider" in str(error)


def test_single_button(dash_duo):
    app = dash.Dash(__name__)

    # Create Dash UI and start the test server

    @ButtonContext.Provider(id='single_button')
    def layout():
        return button_widget_layout()

    widget = layout()
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


def test_multiple_buttons(dash_duo):
    app = dash.Dash(__name__)

    # Create multi-button dash UI and start the test server

    widgets = [ButtonContext.wrap(button_widget_layout, id=id) for id in ['bnt1', 'btn2', 'btn3']]
    app.layout = html.Div(widgets)
    dash_duo.start_server(app)

    # Test code

    def _wait_text(widget, text):
        return dash_duo.wait_for_text_to_equal(widget.container.css_id, text, timeout=4)

    for widget in widgets:

        wait_text = lambda text: _wait_text(widget, text)

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



