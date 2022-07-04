from dash import html, dcc, register_page
from dash_svg import Svg, Path

register_page(__name__, path="/pages/reset-password.html", title="Dash/Flightdeck - Reset password")

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                html.Div([
                    html.P([
                        dcc.Link([
                            Svg([
                                Path(fillRule='evenodd', d='M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z', clipRule='evenodd')
                            ], className='icon icon-xs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
                            "Back to log in"
                        ], href='./sign-in.html', className='d-flex align-items-center justify-content-center')
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
                                        html.Span([
                                            Svg([
                                                Path(fillRule='evenodd', d='M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z', clipRule='evenodd')
                                            ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                        ], className='input-group-text', id='basic-addon2'),
                                        dcc.Input(type='password', placeholder='Password', className='form-control', id='password', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                # Form
                                html.Div([
                                    html.Label("Confirm Password", htmlFor='confirm_password'),
                                    html.Div([
                                        html.Span([
                                            Svg([
                                                Path(fillRule='evenodd', d='M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z', clipRule='evenodd')
                                            ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                        ], className='input-group-text', id='basic-addon2'),
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
