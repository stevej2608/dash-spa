import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc

from dash_spa import register_page

from pages import GLOBAL_WARMING_SLUG, SOLAR_SLUG

register_page(__name__, path=GLOBAL_WARMING_SLUG, title="Dash - Global Warming", short_name='Warming')

global_md = """\
### Global Warming
Global Temperature Time Series. Data are included from the GISS
Surface Temperature (GISTEMP) analysis and the global component
of Climate at a Glance (GCAG). Two datasets are provided:

* Global monthly mean
* Annual mean temperature anomalies in degrees Celsius from 1880 to the present

"""

data = pd.read_csv("pages/data/global-warming.csv")

layout =  html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Markdown(global_md),
                html.A("View details", href='https://datahub.io/core/global-temp#readme', className="btn btn-secondary"),
            ], md=3),
            dbc.Col([

                # https://dash.plot.ly/dash-core-components/graph

                dcc.Graph(
                    figure={
                        "data": [{
                            "y": data['Mean'].tolist(),
                            "x": data['Year'].tolist()
                        }],
                        'layout': {
                            'title': 'Global Temperature Change (&#176;C)',
                            'xaxis': {'title': 'Year'}

                        }
                    },
                    config={'displayModeBar': False},

                ),
            ], md=9),

        ]),
        dbc.Row([
            dbc.Col([
                dcc.Link("State Solar", href=SOLAR_SLUG, className="btn btn-primary float-end")
            ], md=12)

        ])
    ])
