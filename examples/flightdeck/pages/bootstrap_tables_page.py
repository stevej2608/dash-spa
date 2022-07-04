import logging
from dash import html
from dash_spa import register_page

from .components import sideBar, mobileNavBar, topNavBar, footer
from .icons.hero import QUESTION_MARK_ICON, HOME_ICON
from .bootstrap_tables import table1, table2


register_page(__name__, path="/pages/tables/boostrap-tables.html", title="Dash/Flightdeck - Bootstrap Tables")

def breadCrumbs():
    return  html.Nav([
        html.Ol([
            html.Li([
                html.A([
                    HOME_ICON
                ], href='#')
            ], className='breadcrumb-item'),
            html.Li([
                html.A("Tables", href='#')
            ], className='breadcrumb-item'),
            html.Li("Bootstrap tables", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})


def banner():
    return html.Div([
        html.Div([
            html.H1("Bootstrap tables", className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                QUESTION_MARK_ICON,
                "Bootstrap Tables Docs"
            ],
            href='https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/tables/',
            className='btn btn-outline-gray-600 d-inline-flex align-items-center')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')


layout = html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                breadCrumbs(),
                banner()
            ], className='py-4'),
            table1(),
            table2(),
            footer()
        ], className='content')
    ])
