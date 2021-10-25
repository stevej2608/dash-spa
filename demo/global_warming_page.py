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

data = pd.read_csv("demo/data/global-warming.csv")

@spa.route('/warming', title='Warming')
def warming():
    return html.Div([
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
                dcc.Link("State Solar", href=spa.url_for('solar'), className="btn btn-primary float-end")
            ], md=12)

        ])
    ])
