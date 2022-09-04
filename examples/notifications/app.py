from dash import html

from dash_bootstrap_components.themes import BOOTSTRAP
from dash_spa import page_container, DashSPA
from server import serve_app

external_stylesheets = [
    BOOTSTRAP,
    ]

def create_dash():
    app = DashSPA( __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets)
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

# python -m examples.notifications.app

if __name__ == "__main__":
    app = create_app(create_dash)
    serve_app(app, debug=False)