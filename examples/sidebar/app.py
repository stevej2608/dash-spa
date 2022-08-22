from dash_spa.logging import log
import dash_bootstrap_components as dbc

from dash_spa import page_container, DashSPA

from .themes import VOLT
from server import serve_app


external_stylesheets = [
    VOLT,
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    ]

app = DashSPA(__name__, external_stylesheets=external_stylesheets)

# python -m examples.sidebar.app

if __name__ == "__main__":
    log.info('__main__')
    app.layout = page_container
    serve_app(app, path='/welcome')