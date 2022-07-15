from dash import html, dcc
from dash_spa import register_page
from .icons import LOCK_CLOSED_ICON, ARROW_NARROW_LEFT_ICON

register_page(__name__, path="/pages/reset-password", title="Dash/Flightdeck - Reset password", container='full_page')

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                html.Div([
                    html.P([
                        dcc.Link([ARROW_NARROW_LEFT_ICON, "Back to log in"
                        ], href='./sign-in', className='d-flex align-items-center justify-content-center')
                    ], className='text-center'),
                    html.Div([
                        html.Div([
                            html.H1("Reset password", className='h3 mb-4'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Email", htmlFor='email'),
                                    html.Div([
                                        dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', required='', disabled='')
                                    ], className='input-group')
                                ], className='mb-4'),
                                # End of Form
                                # Form
                                html.Div([
                                    html.Label("Your Password", htmlFor='password'),
                                    html.Div([
                                        html.Span(LOCK_CLOSED_ICON, className='input-group-text', id='basic-addon2'),
                                        dcc.Input(type='password', placeholder='Password', className='form-control', id='password', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                # Form
                                html.Div([
                                    html.Label("Confirm Password", htmlFor='confirm_password'),
                                    html.Div([
                                        html.Span(LOCK_CLOSED_ICON, className='input-group-text', id='basic-addon2'),
                                        dcc.Input(type='password', placeholder='Confirm Password', className='form-control', id='confirm_password', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                html.Div([
                                    html.Button("Reset password", type='submit', className='btn btn-gray-800')
                                ], className='d-grid')
                            ], action='#')
                        ], className='bg-white shadow border-0 rounded p-4 p-lg-5 w-100 fmxw-500')
                    ], className='col-12 d-flex align-items-center justify-content-center')
                ], className='row justify-content-center form-bg-image')
            ], className='container')
        ], className='vh-lg-100 mt-5 mt-lg-0 bg-soft d-flex align-items-center')
    ])
])
