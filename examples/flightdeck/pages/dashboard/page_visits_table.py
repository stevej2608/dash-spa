from collections import OrderedDict
from dash import html, dcc
import pandas as pd

from dash_spa.components.table import TableAIO, TableContext
from ..icons import ICON

data = OrderedDict(
 [

    ('Page name',['/demo/admin/index', '/demo/admin/forms', '/demo/admin/util', '/demo/admin/validation', '/demo/admin/modals']),
    ('Page Views',['3,225', '2,987', '2,844', '2,050', '1,483']),
    ('Page Value',['$20', '0', '294', '$147', '$19']),
    ('Bounce rate',['42,55%', '43,24%', '32,35%', '50,87%', '26,12%']),
    ('Bounce change',['Up', 'Down', 'Down', 'Up', 'Down']),
    ]
)


df = pd.DataFrame.from_dict(data)


class PageVisitsTable(TableAIO):

    TABLE_CLASS_NAME = 'table align-items-center table-flush'

    def tableRow(self, index, args):
        name, views, value, rate, change = args.values()
        icon = ICON.ARROW_NARROW_UP if change == "Up" else ICON.ARROW_NARROW_DOWN
        return  html.Tr([
            html.Th(name, className='text-gray-900', scope='row'),
            html.Td(views, className='fw-bolder text-gray-500'),
            html.Td(value, className='fw-bolder text-gray-500'),
            html.Td([
                html.Div([
                    icon,
                    rate
                ], className='d-flex')
            ], className='fw-bolder text-gray-500')
        ])



@TableContext.Provider(id='page_visits_table')
def pageVisitsTable():

    table = PageVisitsTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns])

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Page visits", className='fs-5 fw-bold mb-0')
                    ], className='col'),
                    html.Div([
                        dcc.Link("See all", href='#', className='btn btn-sm btn-primary')
                    ], className='col text-end')
                ], className='row align-items-center')
            ], className='card-header'),
            html.Div(table, className='table-responsive')
        ], className='card border-0 shadow')
    ], className='col-12 mb-4')
