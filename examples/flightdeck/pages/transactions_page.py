from dash import html, register_page
from dash_svg import Svg, Path
from dash_spa.logging import log

from .components import sideBar, mobileNavBar, topNavBar, footer
from .transactions import breadCrumbs, table, tableHeader


register_page(__name__, path="/pages/transactions", title="Dash/Flightdeck - Transactions")

def button(text):
    return html.Button(text, type='button', className='btn btn-sm btn-outline-gray-600')

def newPlanButton():
    return html.A([
        Svg([
            Path(strokeLinecap='round', strokeLinejoin='round', strokeWidth='2', d='M12 6v6m0 0v6m0-6h6m-6 0H6')
        ], className='icon icon-xs me-2', fill='none', stroke='currentColor', viewBox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'),
        "New Plan"
    ], href='#', className='btn btn-sm btn-gray-800 d-inline-flex align-items-center')


def layout(page=1):
    page = int(page)
    #log.info('page=%s', page)
    return html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                html.Div([
                    breadCrumbs(),
                    html.H2("All Orders", className='h4'),
                    html.P("Your web analytics dashboard template.", className='mb-0')
                ], className='d-block mb-4 mb-md-0'),
                html.Div([
                    newPlanButton(),
                    html.Div([
                        button("Share"),
                        button("Export")
                    ], className='btn-group ms-2 ms-lg-3')
                ], className='btn-toolbar mb-2 mb-md-0')

            ], className='d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4'),
            tableHeader(),
            table(page),
            footer()
        ], className='content')
    ])
