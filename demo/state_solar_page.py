from dash import html, dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd

from .demo import blueprint as spa

global_md = """\
### Global Warming
Global Temperature Time Series. Data are included from the GISS 
Surface Temperature (GISTEMP) analysis and the global component 
of Climate at a Glance (GCAG). Two datasets are provided: 

* Global monthly mean
* Annual mean temperature anomalies in degrees Celsius from 1880 to the present

"""

# Taken from Dash example, see:
# https://dash.plot.ly/datatable

df = pd.read_csv('demo/data/solar.csv')

@spa.route('/solar', title='Solar')
def solar():
    return html.Div([
        html.Div([
            html.Div([], className="col-md-2"),
            html.Div([
                html.H2('US Solar Capacity'),
                html.Br(),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
                html.Div(id='output')
            ], className="col-md-8"),
            html.Div([], className="col-md-2")
        ], className='row'),

        dbc.Row([
            dbc.Col([
                dcc.Link("Global Warming", href=spa.url_for('warming'), className="btn btn-primary float-right")
            ], md=12)

        ])

    ], className="container-fluid")
