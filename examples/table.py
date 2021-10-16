import json
from holoniq.utils import logging

from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt
from dash_spa import spa, Blueprint

from app import create_dash
from server import serve_app
import pandas as pd

test = Blueprint('test')

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Col for checkboxes

df.insert(0, '', '')

columns = [{"title": i, "data": i} for i in df.columns]

def button(icon, text, button_type="btn-primary"):
    return html.Div([
        html.Button(html.I(className=f'fa {icon} fa-sm'), title=text, className=f"btn {button_type}")
    ], className="btn-group", role='group')

def toolbar():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        button('fa-refresh', 'Add'),
                        button('fa fa-plus fa-lg', 'Add'),
                        button('fa-eye', 'Add', button_type="btn-warning"),
                    ], className="btn-group btn-group-justified", role='group')
                ], role='toolbar')
            ], className='col-xs-offset 1 col-xs-11 col-sm-offset-2 col-sm-8 col-md-offset-3 col-md-6')
        ], className='row')
    ], className='container')


@test.route('/page1')
def route1():

    table = html.Div([
        html.H2('US Solar Capacity'),
        toolbar(),
        ddt.DashDatatables(
            id='solar',
            columns=columns,

            column_defs = [ {
                'orderable': False,
                'className': 'select-checkbox',
                'targets':   0,
                'width': "4%"          
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

    @test.callback(Output('solar#output', 'children'), [Input('solar', 'table_event')])
    def display_output(value):
        selected = None

        if value and value['action'] == 'selectItems':
            selected = value['indexes']
            selected = format(json.dumps(selected))

        print(f'Select rows: {selected}')
        return f'Select rows: {selected}'

    return html.Div([
        table,
        html.Div(id='solar#output')
    ])


def create_app(dash_factory):
    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    app = spa.SinglePageApp(dash_factory)
    app.register_blueprint(test, url_prefix='/table')

    app.layout()

    return app

#
# python -m examples.table
#

if __name__ == '__main__':
    app = create_app(create_dash)
    serve_app(app.dash,"/table/page1")
