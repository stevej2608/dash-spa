from dash import html, dcc
from dash_spa import register_page
from .icons import ARROW_NARROW_LEFT

register_page(__name__, path="/pages/404", title="Dash/Flightdeck - 404", container='full_page')

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        html.Section([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(className='img-fluid w-75', src='/assets/img/illustrations/404.svg', alt='404 not found'),
                            html.H1([
                                "Page not",
                                html.Span(" found", className='fw-bolder text-primary')
                            ], className='mt-5'),
                            html.P("Oops! Looks like you followed a bad link. If you think this is a problem with us, please tell us.", className='lead my-4'),
                            dcc.Link([ARROW_NARROW_LEFT, "Back to homepage"
                            ], href='dashboard', className='btn btn-gray-800 d-inline-flex align-items-center justify-content-center mb-4')
                        ])
                    ], className='col-12 text-center d-flex align-items-center justify-content-center')
                ], className='row')
            ], className='container')
        ], className='vh-100 d-flex align-items-center justify-content-center')
    ])
])
