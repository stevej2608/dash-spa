from dash_spa.logging import log
from dash import html, register_page
from dash_svg import Svg, Path

from pages import TRANSACTIONS_SLUG
from .transactions import table, tableHeader


register_page(__name__, path=TRANSACTIONS_SLUG, title="Dash/Flightdeck - Transactions", short_name='Transactions')

def button(text):
    return html.Button(text, type='button', className='btn btn-sm btn-outline-gray-600')

def newPlanButton():
    return html.A([
        Svg([
            Path(strokeLinecap='round', strokeLinejoin='round', strokeWidth='2', d='M12 6v6m0 0v6m0-6h6m-6 0H6')
        ], className='icon icon-xs me-2', fill='none', stroke='currentColor', viewBox='0 0 24 24', xmlns='http://www.w3.org/2000/svg'),
        "New Plan"
    ], href='#', className='btn btn-sm btn-gray-800 d-inline-flex align-items-center')


def table_layout(page=1):
    page = int(page)
    #log.info('page=%s', page)
    return html.Div([
        html.Main([
            tableHeader(),
            table(page),
        ], className='content')
    ])

layout = table_layout()
