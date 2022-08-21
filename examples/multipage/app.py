from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_spa import logging

from dash_spa import DashSPA, page_container
from dash_spa.components import NavBar, NavbarBrand, NavbarLink, Footer
from server import serve_app

from .pages import page1, page2

def create_dash():
    app = DashSPA( __name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
    return app

def create_app(dash_factory) -> Dash:
    app = dash_factory()

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
                html.Header([
                    navbar.layout(),
                    html.Br()
                    ]),
                html.Main([
                    html.Div([
                        html.Div([
                            html.Div(page_container, className="col-md-12"),
                        ], className='row')
                    ], className='container d-flex flex-column flex-grow-1'),
                ], role='main', className='d-flex'),
                html.Footer(footer.layout(), className='footer mt-auto')
            ], className='body')

    app.layout = layout
    return app

# python -m examples.multipage.app

if __name__ == "__main__":
    logging.setLevel("INFO")
    app = create_app(create_dash)
    serve_app(app, debug=False)