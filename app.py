import flask
from dash import Dash
import dash_bootstrap_components as dbc
from dash_spa import spa_pages
from dash_spa import config

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    ]

external_scripts = [
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]

def create_dash() -> Dash:

    flask_options = config.get('flask')
    options = config.get('logging')

    server = flask.Flask(__name__)
    server.config['SECRET_KEY'] = flask_options.SECRET_KEY

    app = Dash(__name__,
            plugins=[spa_pages],
            prevent_initial_callbacks=True,
            suppress_callback_exceptions=True,
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts, server=server
            )

    # app.add_stylesheets('css/volt.css')

    app.logger.setLevel(options.level)

    return app

