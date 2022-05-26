from dash_spa.logging import log
from dash import html, register_page
from dash_svg import Svg, Path

from pages import TRANSACTIONS_SLUG
from .transactions import create_table, create_header

from dash_spa.components.table import TableAIOPaginator, TableAIOPaginatorView

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


def _table_layout(page=1):
    page = int(page)
    #log.info('page=%s', page)

    table = create_table(page)
    header = create_header(table)
    paginator = TableAIOPaginator(table, className='pagination mb-0', id="transactions_paginator")
    viewer = TableAIOPaginatorView(table, id="transactions_paginator_view")

    return html.Div([
        header,
        html.Div(table, className='card card-body border-0 shadow table-wrapper table-responsive'),
        html.Div([
            paginator,
            viewer
        ], className='card-footer px-3 border-0 d-flex flex-column flex-lg-row align-items-center justify-content-between')
    ])

layout = _table_layout()
