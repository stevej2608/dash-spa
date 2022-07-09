from dash import html, dcc
from dash_spa import register_page
from .icons import ARROW_NARROW_LEFT_ICON

register_page(__name__, path="/pages/forgot-password.html", title="Dash/Flightdeck - Forgot password")

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                html.Div([
                    html.P([
                        dcc.Link([ ARROW_NARROW_LEFT_ICON,"Back to log in"
                        ], href='./sign-in.html', className='d-flex align-items-center justify-content-center')
                    ], className='text-center'),
                    html.Div([
                        html.Div([
                            html.H1("Forgot your password?", className='h3'),
                            html.P("Don't fret! Just type in your email and we will send you a code to reset your password!", className='mb-4'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Email", htmlFor='email'),
                                    html.Div([
                                        dcc.Input(type='email', className='form-control', id='email', placeholder='john@company.com', required='')
                                    ], className='input-group')
                                ], className='mb-4'),
                                # End of Form
                                html.Div([
                                    html.Button("Recover password", type='submit', className='btn btn-gray-800')
                                ], className='d-grid')
                            ], action='#')
                        ], className='signin-inner my-3 my-lg-0 bg-white shadow border-0 rounded p-4 p-lg-5 w-100 fmxw-500')
                    ], className='col-12 d-flex align-items-center justify-content-center')
                ], className='row justify-content-center form-bg-image')
            ], className='container')
        ], className='vh-lg-100 mt-5 mt-lg-0 bg-soft d-flex align-items-center')
    ])
])
