from dash import html, dcc
from dash_spa import register_page
from .common import background_img
from .icons import ICON

register_page(__name__, path="/pages/lock", title="Dash/Flightdeck - Lock", container='full_page')

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                dcc.Link([ICON.ARROW_NARROW_LEFT, "Back to homepage"
                ], href='dashboard', className='d-flex align-items-center justify-content-center mb-4'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(className='rounded-circle', alt='Image placeholder', src='/assets/img/team/profile-picture-3.jpg')
                                ], className='avatar avatar-lg mx-auto mb-3'),
                                html.H1("Bonnie Green", className='h3'),
                                html.P("Better to be safe than sorry.", className='text-gray')
                            ], className='text-center text-md-center mb-4 mt-md-0'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Password", htmlFor='password'),
                                    html.Div([
                                        html.Span(ICON.LOCK_CLOSED, className='input-group-text', id='basic-addon2'),
                                        dcc.Input(type='password', placeholder='Password', className='form-control', id='password', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                html.Div([
                                    html.Button("Unlock", type='submit', className='btn btn-gray-800')
                                ], className='d-grid mt-3')
                            ], className='mt-5')
                        ], className='bg-white shadow border-0 rounded p-4 p-lg-5 w-100 fmxw-500')
                    ], className='col-12 d-flex align-items-center justify-content-center')
                ], className='row justify-content-center form-bg-image', style=background_img("/assets/img/illustrations/signin.svg"))
            ], className='container')
        ], className='vh-lg-100 mt-5 mt-lg-0 bg-soft d-flex align-items-center')
    ])
])
