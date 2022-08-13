from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_spa import page_container, DashSPA
from server import serve_app


def create_dash():
    app = DashSPA( __name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.server.config['SECRET_KEY'] = "A secret key"
    return app


def create_app(dash_factory) -> DashSPA:
    app = dash_factory()
    def layout():
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(page_container, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
        ])

    app.layout = layout
    return app

# python -m examples.context.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False)
