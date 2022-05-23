from collections import OrderedDict
from dash import html
import pandas as pd
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.table import TableAIO, TableAIOPaginator, TableAIOPaginatorView


data = OrderedDict([
    ('#',['456478', '456423', '456420', '456421', '456420', '456479', '456478', '453673', '456468', '456478']),
    ('Bill For',['Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Platinum Subscription Plan', 'Gold Subscription Plan', 'Gold Subscription Plan', 'Flexible Subscription Plan']),
    ('Issue Date',['1 May 2020', '1 Apr 2020', '1 Mar 2020', '1 Feb 2020', '1 Jan 2020', '1 Dec 2019', '1 Nov 2019', '1 Oct 2019', '1 Sep 2019', '1 Aug 2019']),
    ('Due Date',['1 Jun 2020', '1 May 2020', '1 Apr 2020', '1 Mar 2020', '1 Feb 2020', '1 Jan 2020', '1 Dec 2019', '1 Nov 2019', '1 Oct 2019', '1 Sep 2019']),
    ('Total',['$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$799.00', '$533.42', '$533.42', '$233.42']),
    ('Status',['Due', 'Paid', 'Paid', 'Paid', 'Paid', 'Paid', 'Paid', 'Cancelled', 'Paid', 'Paid']),
    ]
)

def rows():
    _data = OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
    order_numbers = [ n for n in range(400000, 400000 + len(_data['#']))]
    _data['#'] = order_numbers
    return _data

df = pd.DataFrame(rows())


class OrdersTable(TableAIO):

    TABLE_CLASS_NAME = 'card card-body border-0 shadow table-wrapper table-responsive'

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

    def paginator_init(self, page:int, page_size, total_items) -> TableAIOPaginator:

        paginator = TableAIOPaginator(page=page, page_size=page_size, total_items=total_items, className='pagination mb-0')
        viewer = TableAIOPaginatorView(paginator)

        class CompositePaginator():

            @property
            def value(self):
                return self.paginator.store.input.data

            def __init__(self, paginator, viewer):
                self.paginator = paginator
                self.viewer = viewer

            def layout(self, page=1):
                children = [html.Nav(paginator.layout(page=page)), viewer.layout()]
                return html.Div(children, className='card-footer px-3 border-0 d-flex flex-column flex-lg-row align-items-center justify-content-between')

            def state(self, state:dict = None):
                return self.paginator.state(state)

        return CompositePaginator(paginator, viewer)


ordersTable = OrdersTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=7
)

def table(page):
    return ordersTable.layout(page)
