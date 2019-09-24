import os
from utils import config, DashDebug
import dash
import dash_bootstrap_components as dbc

flask_options = config.get('flask')

DASH_DEBUG = 'DASH_DEBUG' in os.environ

_app_create = DashDebug if DASH_DEBUG else dash.Dash

app = _app_create(__name__,
                  suppress_callback_exceptions=True,
                  external_stylesheets=[
                      dbc.themes.BOOTSTRAP,
                      'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
                  ])

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.server.config['SECRET_KEY'] = flask_options.secret_key
