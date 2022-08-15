from dash import html
import pandas as pd

from dash_spa import register_page, prefix
from dash_spa.components import DropdownAIO, TableContext, TableAIO, TableAIOPaginator, TableAIOPaginatorView
from dash_spa.logging import log

from pages import TABLE_EXAMPLE_SLUG

register_page(__name__, path=TABLE_EXAMPLE_SLUG, title="Table Example", short_name='Table')



# Example Of creating a custom table with paginator

df = pd.read_csv('pages/data/subscriptions.csv')

class CustomTable(TableAIO):

    def tableAction(self, row):

        pid = prefix('table_example_row_action')

        button = DropdownAIO.Button([
            html.Span(html.Span(className='fas fa-ellipsis-h icon-dark'), className='icon icon-sm'),
            html.Span("Toggle Dropdown", className='visually-hidden')
        ], className='btn btn-link text-dark dropdown-toggle-split m-0 p-0')

        # Action column dropdown bottom-left. Ripped from the Volt transactions table using Firefox debug tools

        style={"position": "absolute",
                "inset": "0px 0px auto auto",
                "margin": "0px",
                "transform": "translate3d(0px, 25.3333px, 0px)"
                }

        container = html.Div([
            html.A([html.Span(className='fas fa-eye me-2'), "View Details" ], className='dropdown-item rounded-top', href='#'),
            html.A([html.Span(className='fas fa-edit me-2'), "Edit"], className='dropdown-item', href='#'),
            html.A([html.Span(className='fas fa-trash-alt me-2'), "Remove" ], className='dropdown-item text-danger rounded-bottom', href='#')
        ], className='dropdown-menu py-0', style=style)

        return html.Div(DropdownAIO(button, container, id=pid(row)), className='btn-group')


    def tableRow(self, index, args):

        cid, bill, issue_date, due_date, total, status, action, = args.values()
        action = self.tableAction(index)

        return html.Tr([
            html.Td(html.A(cid, href='#', className='fw-bold')),
            html.Td(html.Span(bill, className='fw-normal')),
            html.Td(html.Span(issue_date, className='fw-normal')),
            html.Td(html.Span(due_date, className='fw-normal')),
            html.Td(html.Span(total, className='fw-bold')),
            html.Td(html.Span(status, className='fw-bold text-warning')),
            html.Td(action)
        ])


@TableContext.Provider()
def layout():
    log.info('layout - example_table')
    table = CustomTable(
        data=df.to_dict('records'),
        page_size = 8,
        columns=[{'id': c, 'name': c} for c in df.columns],
        id="table_example")

    paginator = TableAIOPaginator(className='pagination mb-0', id="table_example_paginator")
    viewer = TableAIOPaginatorView()

    paginator_row = html.Div([
        paginator,
        viewer
        ], className='card-footer px-3 border-0 d-flex flex-column flex-lg-row align-items-center justify-content-between')

    return html.Div([
        html.Div(table, className='card card-body border-0 shadow table-wrapper table-responsive'),
        paginator_row
    ])

