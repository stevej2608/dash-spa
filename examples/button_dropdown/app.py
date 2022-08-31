import dash_bootstrap_components as dbc
from dash_spa import page_container, DashSPA
from dash_spa.logging import setLevel

from server import serve_app

def create_dash():
    app = DashSPA( __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.server.config['SECRET_KEY'] = "A secret key"

    return app


def create_app(dash_factory) -> DashSPA:
    app = dash_factory()
    app.layout = page_container
    return app

# python -m examples.button_dropdown.app

if __name__ == "__main__":
    setLevel("INFO")
    app = create_app(create_dash)
    serve_app(app, debug=False)