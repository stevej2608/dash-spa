from dash import html, dcc
from dash_spa import register_page
from dash_svg import Svg, Path

register_page(__name__, path="/pages/500.html", title="Dash/Flightdeck - 500")

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        html.Section([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1([
                            "Something has gone",
                            html.Span(" seriously ", className='text-primary'),
                            "wrong"
                        ], className='mt-5'),
                        html.P("It's always time for a coffee break. We should be back by the time you finish your coffee.", className='lead my-4'),
                        dcc.Link([
                            Svg([
                                Path(fillRule='evenodd', d='M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z', clipRule='evenodd')
                            ], className='icon icon-xs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
                            "Back to homepage"
                        ], href='dashboard.html', className='btn btn-gray-800 d-inline-flex align-items-center justify-content-center mb-4')
                    ], className='col-12 col-lg-5 order-2 order-lg-1 text-center text-lg-left'),
                    html.Div([
                        # html.Img(className='img-fluid w-75', style=background_img('/assets/img/illustrations/500.svg', 416, 390))
                        html.Img(src='/assets/img/illustrations/500.svg')
                    ], className='col-12 col-lg-7 order-1 order-lg-2 text-center d-flex align-items-center justify-content-center')
                ], className='row align-items-center')
            ], className='container')
        ], className='vh-100 d-flex align-items-center justify-content-center')
    ])
])
