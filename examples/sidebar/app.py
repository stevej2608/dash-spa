from dash_spa.logging import setLevel
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
    setLevel("INFO")
    app.layout = page_container
    app.server.config['SECRET_KEY'] = "A secret key"
    serve_app(app)