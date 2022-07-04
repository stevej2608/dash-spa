
from collections import OrderedDict
from dash import html, dcc
from dash_svg import Svg, Path
import pandas as pd

from dash_spa.components.table import TableAIO, TableContext

data = OrderedDict(
 [

    ('Page name',['/demo/admin/index.html', '/demo/admin/forms.html', '/demo/admin/util.html', '/demo/admin/validation.html', '/demo/admin/modals.html']),
    ('Page Views',['3,225', '2,987', '2,844', '2,050', '1,483']),
    ('Page Value',['$20', '0', '294', '$147', '$19']),
    ('Bounce rate',['42,55%', '43,24%', '32,35%', '50,87%', '26,12%']),
    ('Bounce change',['Up', 'Down', 'Down', 'Up', 'Down']),
    ]
)


df = pd.DataFrame.from_dict(data)

UP_ICON = Svg([
        Path(fillRule='evenodd', d='M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L6.707 7.707a1 1 0 01-1.414 0z', clipRule='evenodd')
    ], className='icon icon-xs text-danger me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')

DOWN_ICON = Svg([
        Path(fillRule='evenodd', d='M14.707 12.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l2.293-2.293a1 1 0 011.414 0z', clipRule='evenodd')
    ], className='icon icon-xs text-success me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')


class PageVisitsTable(TableAIO):

    TABLE_CLASS_NAME = 'table align-items-center table-flush'

    def tableRow(self, index, args):
        name, views, value, rate, change = args.values()
        icon = UP_ICON if change == "Up" else DOWN_ICON
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
