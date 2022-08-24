from dash import Dash, html
import dash_bootstrap_components as dbc

from dash_spa import page_container, DashSPA, dash_logging
from dash_spa.logging import setLevel

from server import serve_app

def create_dash():
    app = DashSPA( __name__,
        # plugins=[dash_logging],
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app


def create_app(dash_factory) -> DashSPA:
    app = dash_factory()
    def layout():
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(page_container, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
        ])

    app.layout = page_container
    return app

# python -m examples.button_test_redux.app

if __name__ == "__main__":
    setLevel("INFO")
    app = create_app(create_dash)
    serve_app(app, debug=False)