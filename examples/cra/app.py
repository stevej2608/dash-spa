import dash
from dash_spa import page_container
from server import serve_app

app = dash.Dash( __name__, use_pages = True)

# python -m examples.cra.app

if __name__ == "__main__":
    app.layout=page_container
    serve_app(app, debug=False)