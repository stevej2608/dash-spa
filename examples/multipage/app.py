import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_spa import logging

from dash_spa import register_page, NavBar, NavbarBrand, NavbarLink, Footer, page_container, spa_pages
from dash_spa.utils import DashLogger, DEBUG_LEVEL
from server import serve_app


def create_dash():
    app = dash.Dash( __name__, plugins=[spa_pages], external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app

def big_center(text, id=None):
    className='display-3 text-center'
    return html.H2(text, id=id, className=className) if id else html.H2(text, className=className)

def page1_layout():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 1', id="page"),
    ])

def page2_layout():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 2', id="page"),
    ])


def create_app(dash_factory) -> Dash:
    app = dash_factory()

    page1 = register_page(path='/page1', title="Page-1", layout=page1_layout)
    page2 = register_page(path='/page2', title="Page-2", layout=page2_layout)

    NAV_BAR_ITEMS = {
        'brand' : NavbarBrand(' Dash/SPA','/'),
        'left' : [
            NavbarLink(page1, id='nav-page1'),
            NavbarLink(page2, id='nav-page2'),
        ]
    }

    navbar = NavBar(NAV_BAR_ITEMS)
    footer = Footer('SPA/Examples')

    def layout():
        return html.Div([
            navbar.layout(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(page_container, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
            html.Div(id='null'),
            html.Div(footer.layout())
        ])

    app.layout = layout
    return app

# python -m examples.multipage.app

if __name__ == "__main__":
    logging.setLevel("INFO")
    app = create_app(create_dash)
    logger = DashLogger(DEBUG_LEVEL.VERBOSE)
    serve_app(app, debug=False, logger=logger)