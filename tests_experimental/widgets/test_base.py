from dash import html
from dash import Dash, callback
from dash_spa.spa_widget import SPAWidget
from dash_spa.spa_context import createContext, ContextState, dataclass
from dash_spa.logging import log
from dash_spa.utils.dumps_layout import dumps_layout


class MyWidget(html.Div, SPAWidget):

    def __init__(self):
        pfx = self.prefix()
        log.info('MyWidget %s - constructor', pfx())

        self.btn = html.Button("Button", id=pfx('btn'))
        self.div = html.Div("Button pressed 0 times!", id=pfx('div'))

        @callback(self.div.output.children, self.btn.input.n_clicks, prevent_initial_call=True)
        def btn_click(clicks):
            return f"Button pressed {clicks} times!"

        super().__init__([self.btn, self.div])



myWidget = MyWidget()

def test_widget_base(dash_duo):
    app = Dash(__name__)
    app.layout = myWidget

    dash_duo.start_server(app)

    def browser_wait_text(text):
        return dash_duo.wait_for_text_to_equal(myWidget.div.css_id, text, timeout=4)

    assert browser_wait_text("Button pressed 0 times!")

    browser_btn = dash_duo.find_element(myWidget.btn.css_id)
    browser_btn.click()
    assert browser_wait_text("Button pressed 1 times!")


