from dash_spa.logging import log
import dash
from dash import html
import dash_bootstrap_components as dbc

from dash_spa import page_container
from server import serve_app

from .pages.common import store

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
    ]

app = dash.Dash( __name__,
                external_stylesheets=external_stylesheets,
                use_pages = True
                )

def layout():
    """Top level layout, all pages are rendered in the container
    """

    log.info('top level layout()')

    return html.Div([
        store,
        html.Div([
            html.Div([
                html.Div([], className="col-md-1"),
                html.Div(page_container, id='page-content', className="col-md-10"),
                html.Div([], className="col-md-1")
            ], className='row')
        ], className="container-fluid")
    ])

# python -m examples.forms.app

if __name__ == "__main__":
    log.info('__main__')
    app.layout = layout()
    serve_app(app, path='/login')