import dash
from dash_spa import page_container, spa_pages
from server import serve_app

app = dash.Dash( __name__, plugins=[spa_pages])

# python -m examples.cra.app

if __name__ == "__main__":
    app.layout=page_container
    serve_app(app, debug=False)