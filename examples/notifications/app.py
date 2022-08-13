import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

from dash_spa import page_container, DashSPA

from themes import VOLT
from server import serve_app


external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/chartist/0.11.4/chartist.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.2.0/css/all.min.css",
    VOLT,
    ]

external_scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]

def create_dash():
    app = DashSPA( __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_scripts=external_scripts,
        external_stylesheets=external_stylesheets)
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

    app.layout = layout
    return app

# python -m examples.notifications.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False)