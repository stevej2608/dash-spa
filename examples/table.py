from utils import logging, log
from dash import html
import dash_datatables as ddt

from dash_spa import spa, Blueprint

from app import app as dash_app
from server import serve_app

test = Blueprint('test')

import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

column_defs = [{"title": i, "data": i} for i in df.columns]

@test.route('/page1')
def route1():
    spa = test.get_spa('page1')

    table = html.Div([
        html.H2('US Solar Capacity'),
        html.Br(),
        ddt.DashDatatables(
            columns=column_defs,
            data=df.to_dict('records'),
            width="100%",
            order=[2, 'asc'],
        )
    ])

    return html.Div([
        table
    ])


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
