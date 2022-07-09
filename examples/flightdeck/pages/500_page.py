from dash import html, dcc
from dash_spa import register_page
from .icons import ARROW_NARROW_LEFT_ICON

register_page(__name__, path="/pages/500.html", title="Dash/Flightdeck - 500", container='full_page')

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
                        dcc.Link([ARROW_NARROW_LEFT_ICON, "Back to homepage"
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
