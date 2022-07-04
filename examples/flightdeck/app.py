import dash
from dash import Dash
import dash_spa as spa
from dash_spa.themes import VOLT, VOLT_BOOTSTRAP
from server import serve_app

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/chartist/0.11.4/chartist.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.2.0/css/all.min.css",
    VOLT_BOOTSTRAP,
    ]

external_scripts = [
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]


def create_dash():

    plugins=[
        spa.spa_session,
        spa.spa_pages
        ]

    app = dash.Dash( __name__,
        plugins=plugins,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets)
    return app


def create_app(dash_factory) -> Dash:
    app = dash_factory()

    def layout():
        return spa.page_container

    app.layout = layout
    return app

# python -m examples.flightdeck.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False, path="/pages/dashboard.html")
