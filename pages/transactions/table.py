from dash import html
import pandas as pd
from dash_spa import prefix
from dash_spa.logging import log
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.table import TableAIO

from dash_spa.components.table import TableContext, filter_str

#
# https://json-generator.com/#
# https://www.convertcsv.com/json-to-csv.htm
#
# [
#   '{{repeat(300, 300)}}',
#   {
#     index: '{{index()}}',
#     isActive: '{{bool()}}',
#     balance: '{{floating(1000, 4000, 2, "$0,0.00")}}',
#     age: '{{integer(20, 40)}}',
#     eyeColor: '{{random("blue", "brown", "green")}}',
#     name: '{{firstName()}} {{surname()}}',
#     gender: '{{gender()}}',
#     company: '{{company().toUpperCase()}}',
#     email: '{{email()}}',
#     phone: '+1 {{phone()}}',
#     address: '{{integer(100, 999)}} {{street()}}, {{city()}}, {{state()}}, {{integer(100, 10000)}}',
#     registered: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
#   }
# ]

df = pd.read_csv('pages/data/customers.csv')


class OrdersTable(TableAIO):

    def tableAction(self, row):

        pid = prefix('orders_table_row_action')

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


    def tableRow(self, row_index, args):

        # cid, active, balance, age, eyes, name, gender, company, email, phone, address, registered = args.values()
        cid, active, balance, age, name, company = args.values()

        active = 'yes' if active else ''
        action = self.tableAction(row_index)

        return html.Tr([
            html.Td(html.A(cid, href='#', className='fw-bold')),
            html.Td(html.Span(active, className='fw-normal')),
            html.Td(html.Span(balance, className='fw-normal')),
            html.Td(html.Span(age, className='fw-normal')),
            html.Td(html.Span(name, className='fw-normal')),
            html.Td(html.Span(company, className='fw-bold')),
            html.Td(action)
        ])


def create_table(id) -> OrdersTable:

    # TODO: Cache previous df search results

    # [index, isActive, balance, age, eyeColor, name, gender, company, email, phone, address, registered]

    df1 = df[['index', 'isActive', 'balance', 'age', 'name', 'company']]

    state = TableContext.getState()

    df1 = filter_str(df1, state.search_term)

    log.info("create_table %s %s", id, state)

    ordersTable = OrdersTable(
        data=df1.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df1.columns],
        page = state.current_page,
        page_size = state.page_size,
        id=id
    )

    return ordersTable

