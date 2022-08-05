import dash
from dash_spa import page_container, spa_pages
from server import serve_app

external_stylesheets = [
    "https://fonts.googleapis.com/css?family=Roboto:300,400,700",
    "https://res.cloudinary.com/sivadass/image/upload/v1494699523/icons/bare-tree.png",
    ]


app = dash.Dash( __name__,
        plugins=[spa_pages],
        external_stylesheets=external_stylesheets,
        )

# python -m examples.veggy.app

if __name__ == "__main__":
    app.layout=page_container
    serve_app(app, debug=False)