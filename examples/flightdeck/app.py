import flask
from dash import Dash
import dash_labs as dl
from components.store_aio import StoreAIO

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/chartist/0.11.4/chartist.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.2.0/css/all.min.css"
    ]

external_scripts = [
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]


def create_app(layout, scripts=external_scripts, stylesheets=external_stylesheets, plugins=[dl.plugins.pages]) -> Dash:
    # Server definition

    server = flask.Flask(__name__)
    app = Dash(__name__,
            plugins=plugins,
            external_stylesheets=stylesheets,
            external_scripts=scripts, server=server)

    if layout == dl.plugins.page_container:
        dl.plugins.page_container.children.insert(0, StoreAIO.container)

    app.layout = layout

    return app
