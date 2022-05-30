import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_spa import logging

from dash_spa import page_container, spa_pages
from dash_spa.utils import DashLogger, DEBUG_LEVEL
from server import serve_app


def create_dash():
    app = dash.Dash( __name__,
        plugins=[spa_pages],
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.server.config['SECRET_KEY'] = "A secret key"
    return app


def create_app(dash_factory) -> Dash:
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

    app.layout = layout
    return app

# python -m examples.react_pattern.app

if __name__ == "__main__":
    logging.setLevel("INFO")
    app = create_app(create_dash)

    serve_app(app, debug=False)

    # logger = DashLogger(DEBUG_LEVEL.VERBOSE)
    # serve_app(app, debug=False, logger=logger)