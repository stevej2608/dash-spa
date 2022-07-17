from dash import html

from ..icons.hero import ICON


def acquisition():
    return html.Div([
        html.Div([
            html.Div([
                html.H2("Acquisition", className='fs-5 fw-bold mb-1'),
                html.P("Tells you where your visitors originated from, such as search engines, social networks or website referrals."),
                html.Div([
                    html.Div([
                        html.Div([
                            ICON.CHART
                       ], className='icon-shape icon-sm icon-shape-danger rounded me-3'),
                        html.Div([
                            html.Label("Bounce Rate", className='mb-0'),
                            html.H4("33.50%", className='mb-0')
                        ], className='d-block')
                    ], className='d-flex align-items-center me-5'),
                    html.Div([
                        html.Div([
                            ICON.BARCHART
                        ], className='icon-shape icon-sm icon-shape-purple rounded me-3'),
                        html.Div([
                            html.Label("Sessions", className='mb-0'),
                            html.H4("9,567", className='mb-0')
                        ], className='d-block')
                    ], className='d-flex align-items-center pt-3')
                ], className='d-block')
            ], className='card-body')
        ], className='card border-0 shadow')
    ], className='col-12 px-0')

