import logging
from dash import html
from dash_spa import register_page

from .common import breadCrumbs, sideBar, mobileNavBar, topNavBar, footer
from .icons.hero import QUESTION_MARK_ICON, HOME_ICON
from .bootstrap_tables import table1, table2


register_page(__name__, path="/pages/tables/boostrap-tables.html", title="Dash/Flightdeck - Bootstrap Tables")

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
                breadCrumbs(["Tables","Bootstrap tables"]),
                banner()
            ], className='py-4'),
            table1(),
            table2(),
            footer()
        ], className='content')
    ])