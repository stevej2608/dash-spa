from dash import html, dcc
from dash_spa import register_page
from .icons import LOCK_CLOSED_ICON, MAIL_ICON, ARROW_NARROW_LEFT_ICON, FACEBOOK_ICON, TWITTER_ICON, GITHUB_ICON

register_page(__name__, path="/pages/sign-up.html", title="Dash/Flightdeck - Sign up", container='full_page')


layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                html.P([
                    dcc.Link([ARROW_NARROW_LEFT_ICON,"Back to homepage"], href='dashboard.html', className='d-flex align-items-center justify-content-center')
                ], className='text-center'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H1("Create Account", className='mb-0 h3')
                            ], className='text-center text-md-center mb-4 mt-md-0'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Email", htmlFor='email'),
                                    html.Div([
                                        html.Span(MAIL_ICON, className='input-group-text', id='basic-addon1'),
                                        dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', autoFocus='', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                html.Div([
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
                                        html.Div([
                                            dcc.Input(className='form-check-input', type='checkbox', value='', id='remember'),
                                            html.Label([
                                                "I agree to the",
                                                dcc.Link("terms and conditions", href='#', className='fw-bold')
                                            ], className='form-check-label fw-normal mb-0', htmlFor='remember')
                                        ], className='form-check')
                                    ], className='mb-4')
                                ], className='form-group'),
                                html.Div([
                                    html.Button("Sign up", type='submit', className='btn btn-gray-800')
                                ], className='d-grid')
                            ], action='#', className='mt-4'),
                            html.Div([
                                html.Span("or login with", className='fw-normal')
                            ], className='mt-3 mb-4 text-center'),
                            html.Div([
                                dcc.Link(FACEBOOK_ICON.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button'),
                                dcc.Link(TWITTER_ICON.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button'),
                                dcc.Link(GITHUB_ICON.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button')
                            ], className='d-flex justify-content-center my-4'),
                            html.Div([
                                html.Span([
                                    "Already have an account?",
                                    dcc.Link("Login here", href='./sign-in.html', className='fw-bold')
                                ], className='fw-normal')
                            ], className='d-flex justify-content-center align-items-center mt-4')
                        ], className='bg-white shadow border-0 rounded border-light p-4 p-lg-5 w-100 fmxw-500')
                    ], className='col-12 d-flex align-items-center justify-content-center')
                ], className='row justify-content-center form-bg-image', **{"data-background-lg": "../../assets/img/illustrations/signin.svg"})
            ], className='container')
        ], className='vh-lg-100 mt-5 mt-lg-0 bg-soft d-flex align-items-center')
    ])
])
