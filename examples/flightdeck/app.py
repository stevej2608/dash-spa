import dash
from dash import Dash
from dash_spa import page_container, spa_pages
from server import serve_app

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/chartist/0.11.4/chartist.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.2.0/css/all.min.css"
    ]

external_scripts = [
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]


def create_dash():
    app = dash.Dash( __name__,
        plugins=[spa_pages],
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets)
    return app


def create_app(dash_factory) -> Dash:
    app = dash_factory()

    def layout():
        return page_container

    app.layout = layout
    return app

# python -m examples.flightdeck.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False)
