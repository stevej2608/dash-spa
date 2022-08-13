import dash
from dash_spa import page_container, DashSPA
from server import serve_app

app = DashSPA( __name__)

# python -m examples.cra.app

if __name__ == "__main__":
    app.layout=page_container
    serve_app(app, debug=False)