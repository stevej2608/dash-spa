from collections import OrderedDict
from dash import html
import pandas as pd
from dash_spa import NOUPDATE
from dash_spa.logging import log
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.components.table import TableAIO

from dash_spa.local_storage import SPA_CONFIG


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


    def get_config(self):
        ID = 'transactions'
        config = SPA_CONFIG.get_config(ID)
        if config:
            return config
        else:
            return super().get_config()

    def init(self):

        ID = 'transactions'

        # Triggered by SPA_CONFIG changes, pass the config to the
        # transaction table. This happens on startup to restore the
        # table configuration
        #
        #  Browser local storage -> table

        # @self.table_config.update(SPA_CONFIG.input.data)
        # def _table_update(spa_config, table_config):
        #     if spa_config:
        #         table_config = SPA_CONFIG.get_user(ID, spa_config)
        #         log.info('SPA config read, saved table_config=%s', spa_config)
        #         return table_config
        #     else:
        #         log.info('SPA config read - NOUPDATE')
        #         return NOUPDATE

        # Triggered by user changes to the table settings, write the changes
        # to SPA_CONFIG
        #
        # Table settings change -> Browser local storage

        @SPA_CONFIG.update(self.table_config.input.data)
        def _local_update(table_config, spa_config):
            if table_config:
                log.info('SPA config write %s', table_config)
                store = SPA_CONFIG.set_user(ID, spa_config, table_config)
                return store
            else:
                log.info('SPA config write NOUPDATE')
                NOUPDATE

def create_table(page) -> OrdersTable:
    ordersTable = OrdersTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        page = page,
        id="transactions_table"
    )

    return ordersTable

