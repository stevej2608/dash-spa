from dash import Dash, html
from dash_spa import prefix

# Test 1: Component prefix works

def test_module_component_prefix():
    app = Dash(__name__)
    pfx = prefix('test123')
    div = html.H2('Hello World', id=pfx('hello'))

    app.callback(div.output.children,div.input.n_clicks)
    def _callback(clicks):
        return None

    assert div.id == 'test123_hello'
