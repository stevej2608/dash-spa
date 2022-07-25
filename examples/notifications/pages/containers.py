import traceback
from dash import html
import dash_spa as spa
from pages import NAVBAR_PAGES
from dash_spa.logging import log
from dash_spa_admin import AdminNavbarComponent
from dash_spa.exceptions import InvalidAccess

def default_container(page, layout,  **kwargs):

    content = layout(**kwargs) if callable(layout) else layout

    return html.Div([
        html.Br(),
        html.Div(
            html.Div([
                html.Div(content, className="col-10"),
                html.Div(className="col-2")
            ], className='row'),
            className='container')
        ])


spa.register_container(default_container)
