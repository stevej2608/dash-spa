from dash import Dash, html
from dash_spa import spa, Blueprint

def create_spa(blueprint):
    """Create and layout Dash/SPA app"""
    def dash_factory():
        return Dash(__name__)

    app = spa.SinglePageApp(dash_factory)
    app.register_blueprint(blueprint, url_prefix='/test')
    app.layout()
    return app

# Test 1: Component prefix is derived from __NAME__

def test_module_component_prefix():
    app = Dash(__name__)
    div = html.H2('Hello World', id='hello')

    app.callback(div.output.children,div.input.n_clicks)
    def _callback(clicks):
        return None

    assert div.id == 'tests-spa-spa_prefix_test-hello'

# Test 2: Component prefix with ctx defined is {blueprint}.{route}

def test_bluprint_component_prefix():

    div = None

    # Create Dash/SPA blueprint

    test = Blueprint('test')

    @test.route('/ticker', title='Ticker')
    def ticker(ctx):
        nonlocal div

        div = html.H2('Hello World', id='hello')

        test.callback(div.output.children,div.input.n_clicks)
        def _callback(clicks):
            return None

    # Create and layout Dash/SPA app

    create_spa(test)

    # Confirm the component prefix is {blueprint}.{route}

    assert div.id == 'test-ticker-hello'

# Test 3 : With ctx undefined the applied prefix defaults to __NAME__

def test_bluprint_component_with_module_prefix():

    div = None

    # Create Dash/SPA blueprint

    test = Blueprint('test')

    @test.route('/ticker', title='Ticker')
    def ticker():
        nonlocal div

        div = html.H2('Hello World', id='hello')

        test.callback(div.output.children,div.input.n_clicks)
        def _callback(clicks):
            return None

    # Create and layout Dash/SPA app

    create_spa(test)

    # Confirm the component prefix is {blueprint}.{route}

    assert div.id == 'tests-spa-spa_prefix_test-hello'

# Test 4: With route attribute prefix_ids=False no prefix is applied

def test_bluprint_component_with_no_prefix():

    div = None

    # Create Dash/SPA blueprint

    test = Blueprint('test')

    @test.route('/ticker', title='Ticker', prefix_ids=False)
    def ticker(ctx):
        nonlocal div

        div = html.H2('Hello World', id='hello')

        test.callback(div.output.children,div.input.n_clicks)
        def _callback(clicks):
            return None

    # Create and layout Dash/SPA app

    create_spa(test)

    # Confirm the component prefix is {blueprint}.{route}

    assert div.id == 'hello'
