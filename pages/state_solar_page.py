from dash import html, dcc
import dash_bootstrap_components as dbc

from dash_spa import register_page
from pages import SOLAR_SLUG, GLOBAL_WARMING_SLUG

register_page(__name__, path=SOLAR_SLUG, title="Dash Solar", short_name='Solar')

import pandas as pd

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

df = pd.read_csv('pages/data/solar.csv')

layout = html.Div([
        html.Div([
            html.Div([], className="col-md-2"),
            html.Div([
                html.H2('US Solar Capacity'),
                html.Br(),
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
            ], className="col-md-8"),
            html.Div([], className="col-md-2")
        ], className='row'),

        dbc.Row([
            dbc.Col([
                dcc.Link("Global Warming", href=GLOBAL_WARMING_SLUG, className="btn btn-primary float-end")
            ], md=12)

        ])

    ], className="container-fluid")
