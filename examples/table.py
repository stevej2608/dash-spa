import json
from utils import logging

from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt
from dash_spa import spa, Blueprint

from app import app as dash_app
from server import serve_app
import pandas as pd

test = Blueprint('test')


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

df.insert(0, '', '')

columns = [{"title": i, "data": i} for i in df.columns]

@test.route('/page1')
def route1():
    spa = test.get_spa('page1')

    table = html.Div([
        html.H2('US Solar Capacity'),
        ddt.DashDatatables(
            id='solar',
            columns=columns,

            column_defs = [ {
                'orderable': False,
                'className': 'select-checkbox',
                'targets':   0
                }],

            select = {
                'style':    'os',
                'selector': 'td:first-child'
                },

            data=df.to_dict('records'),
            width="100%",
            order=[2, 'asc'],
        )
    ])

    return html.Div([
        table,
        html.Div(id='solar#output')        
    ])

@dash_app.callback(Output('solar#output', 'children'), [Input('solar', 'table_event')])
def display_output(value):
    selected = None

    if value and value['action'] == 'selectItems':
        selected = value['indexes']
        selected = format(json.dumps(selected))

    print(f'Select rows: {selected}')
    return f'Select rows: {selected}'


def create_app():
    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    app = spa.SinglePageApp(dash_app)
    app.register_blueprint(test, url_prefix='/table')

    app.layout()

    return app.dash.server

#
# python -m examples.table
#

if __name__ == '__main__':
    app = create_app()
    serve_app(app,"/table/page1")
