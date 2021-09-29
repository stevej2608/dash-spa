import dash_datatables as ddt
import pandas as pd
from dash import html
from .view_common import blueprint as admin

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

df.insert(0, '', '')

columns = [{"title": i, "data": i} for i in df.columns]

class InvalidAccess(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def validate_user(ctx):
    login_manager = ctx.login_manager
    if login_manager.isAdmin():
        return True
    raise InvalidAccess("Must be signed in as admin")

@admin.route('/users', title='Admin Users', access=validate_user)
def user_view(ctx):
    spa = admin.get_spa()

    login_manager = ctx.login_manager

    # users = login_manager.users()

    df = pd.read_sql_table('user', login_manager.database_uri())
    df = df.drop(['password'], axis=1)
    df.insert(0, '', '')
    columns = [{"title": i, "data": i} for i in df.columns]

    table = html.Div([
        html.H2('Users'),
        ddt.DashDatatables(
            id='users',
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
            #editable=True
        )
    ])

    return html.Div([
        table,
        spa.Div(id='output')
    ])
