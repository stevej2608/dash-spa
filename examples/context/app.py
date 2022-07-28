import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

from dash_spa import page_container, spa_pages
from dash_spa.session import spa_session
from dash_spa.logging import log
from server import serve_app


def create_dash():
    app = dash.Dash( __name__,
        plugins=[spa_pages, spa_session],
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

# python -m examples.context.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False)
