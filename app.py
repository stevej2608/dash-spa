import flask
from dash import Dash
import dash_bootstrap_components as dbc
import dash_spa as spa
# from dash_spa import spa_pages
# from dash_spa import themes

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css",
    spa.themes.VOLT_BOOTSTRAP,
    spa.themes.VOLT_BOOTSTRAP,
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/chartist/0.11.4/chartist.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.2.0/css/all.min.css"
    ]

external_scripts = [
    # "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/js/bootstrap.bundle.min.js",
    ]


logging_opt = spa.config.get('logging')

def create_dash() -> Dash:

    flask_options = spa.config.get('flask')
    options = spa.config.get('logging')

    server = flask.Flask(__name__)
    server.config['SECRET_KEY'] = flask_options.SECRET_KEY

    plugins=[
        spa.spa_session,
        spa.spa_pages
        ]

    if logging_opt.get('DASH_LOGGING', default=False):
        plugins.append(spa.dash_logging)


    app = Dash(__name__,
            plugins=plugins,
            prevent_initial_callbacks=True,
            suppress_callback_exceptions=True,
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts, server=server
            )

    # app.add_stylesheets('css/volt.css')

    app.logger.setLevel(options.level)

    return app

