from utils import config
import dash
import dash_bootstrap_components as dbc

flask_options = config.get('flask')

app = dash.Dash(__name__,
                  suppress_callback_exceptions=True,
                  external_stylesheets=[
                      dbc.themes.BOOTSTRAP,
                      'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'
                  ])

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.server.config['SECRET_KEY'] = flask_options.secret_key
