from dash import html
import pandas as pd
from collections import OrderedDict

from dash_spa import register_page
from pages import TABLE_EXAMPLE_SLUG

from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.table import TableAIO, TableAIOPaginator, TableAIOPaginatorView

register_page(__name__, path=TABLE_EXAMPLE_SLUG, title="Table Example", short_name='Table')

# Example Of creating a custom table with paginator
#
#       python -m components.table.table_example

data = OrderedDict([
    ('#',['456478', '456423', '456420', '456421', '456420', '456479', '456478', '453673', '456468', '456478']),
    ('Bill For',['Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Gold Subscription Plan', 'Gold Subscription Plan', 'Flexible Subscription Plan']),
    ('Issue Date',['1 May 2020', '1 Apr 2020', '1 Mar 2020', '1 Feb 2020', '1 Jan 2020', '1 Dec 2019', '1 Nov 2019', '1 Oct 2019', '1 Sep 2019', '1 Aug 2019']),
    ('Due Date',['1 Jun 2020', '1 May 2020', '1 Apr 2020', '1 Mar 2020', '1 Feb 2020', '1 Jan 2020', '1 Dec 2019', '1 Nov 2019', '1 Oct 2019', '1 Sep 2019']),
    ('Total',['$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$533.42', '$533.42', '$233.42']),
    ('Status',['Due', 'Paid', 'Paid', 'Paid', 'Paid', 'Paid', 'Paid', 'Cancelled', 'Paid', 'Paid']),
    ]
)

df = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
)

class CustomTable(TableAIO):

    def tableAction(self):

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

        return html.Div(DropdownAIO(button, container), className='btn-group')


    def tableRow(self, args):

        cid, product, issue_date, due_date, total, status = args.values()
        action = self.tableAction()

        return html.Tr([
            html.Td(html.A(cid, href='#', className='fw-bold')),
            html.Td(html.Span(product, className='fw-normal')),
            html.Td(html.Span(issue_date, className='fw-normal')),
            html.Td(html.Span(due_date, className='fw-normal')),
            html.Td(html.Span(total, className='fw-bold')),
            html.Td(html.Span(status, className='fw-bold text-warning')),
            html.Td(action)
        ])


def table_layout():

    table = CustomTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        page_size=7,
        id="table_example")

    paginator = TableAIOPaginator(table.store, className='pagination mb-0', id="table_example_paginator")
    viewer = TableAIOPaginatorView(table.store, id="table_example_paginator_view")
    paginator_row = html.Div([paginator, viewer], className='card-footer px-3 border-0 d-flex flex-column flex-lg-row align-items-center justify-content-between')

    return html.Div([
        html.Div(table, className='card card-body border-0 shadow table-wrapper table-responsive'),
        paginator_row
        ])

layout = table_layout()
