from dash import html, dcc, register_page
from dash_svg import Svg, Path

register_page(__name__, path="/pages/404.html", title="Dash/Flightdeck - 404")

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
                            dcc.Link([
                                Svg([
                                    Path(fillRule='evenodd', d='M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z', clipRule='evenodd')
                                ], className='icon icon-xs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
                                "Back to homepage"
                            ], href='dashboard.html', className='btn btn-gray-800 d-inline-flex align-items-center justify-content-center mb-4')
                        ])
                    ], className='col-12 text-center d-flex align-items-center justify-content-center')
                ], className='row')
            ], className='container')
        ], className='vh-100 d-flex align-items-center justify-content-center')
    ])
])
