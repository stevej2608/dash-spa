from dash import html, dcc
from dash_spa import register_page
from ..common import breadCrumbs, banner, topNavBar, footer

from ..icons import ICON, FACEBOOK, TWITTER, GITHUB

register_page(__name__, path="/pages/components/modals", title="Dash/Flightdeck - Modals")

def default():
    return  html.Div([
        # Button Modal
        html.Button("Default", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-default"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H2("Terms of Service", className='h6 modal-title'),
                        html.Button(type='button', className='btn-close', **{"data-bs-dismiss": "modal", "aria-label": "Close"})
                    ], className='modal-header'),
                    html.Div([
                        html.P("With less than a month to go before the European Union enacts new consumer privacy laws for its citizens, companies around the world are updating their terms of service agreements to comply."),
                        html.P("The European Union’s General Data Protection Regulation (G.D.P.R.) goes into effect on May 25 and is meant to ensure a common set of data rights in the European Union. It requires organizations to notify users as soon as possible of high-risk data breaches that could personally affect them.")
                    ], className='modal-body'),
                    html.Div([
                        html.Button("Accept", type='button', className='btn btn-secondary'),
                        html.Button("Close", type='button', className='btn btn-link text-gray-600 ms-auto', **{"data-bs-dismiss": "modal"})
                    ], className='modal-footer')
                ], className='modal-content')
            ], className='modal-dialog modal-dialog-centered', role='document')
        ], className='modal fade', id='modal-default', role='dialog', **{"aria-labelledby": "modal-default", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')

def notification():
    return html.Div([
        # Button Modal
        html.Button("Notification", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-notification"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Button(type='button', className='btn-close theme-settings-close fs-6 ms-auto', **{"data-bs-dismiss": "modal", "aria-label": "Close"}),
                    html.Div([
                        html.P("A new experience, personalized for you.", className='modal-title text-gray-200', id='modal-title-notification')
                    ], className='modal-header'),
                    html.Div([
                        html.Div([
                            html.Span(ICON.INBOX_IN, className='modal-icon'),
                            html.H2("Important message!", className='h4 modal-title my-3'),
                            html.P("Do you know that you can assign status and relation to a company right in the visit list?")
                        ], className='py-3 text-center')
                    ], className='modal-body text-white'),
                    html.Div([
                        html.Button("Go to Inbox", type='button', className='btn btn-sm btn-white')
                    ], className='modal-footer')
                ], className='modal-content bg-gradient-secondary')
            ], className='modal-dialog modal-info modal-dialog-centered', role='document')
        ], className='modal fade', id='modal-notification', role='dialog', **{"aria-labelledby": "modal-notification", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')

def sign_in():
    return  html.Div([
        # Button Modal
        html.Button("Sign In", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-form"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Button(type='button', className='btn-close ms-auto', **{"data-bs-dismiss": "modal", "aria-label": "Close"}),
                            html.Div([
                                html.H1("Sign in to our platform", className='mb-0 h4')
                            ], className='text-center text-md-center mb-4 mt-md-0'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Email", htmlFor='email'),
                                    html.Div([
                                        html.Span(ICON.MAIL, className='input-group-text', id='basic-addon1'),
                                        dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                html.Div([
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
                                        html.Div([
                                            dcc.Input(className='form-check-input', type='checkbox', value='', id='remember'),
                                            html.Label("Remember me", className='form-check-label mb-0', htmlFor='remember')
                                        ], className='form-check'),
                                        html.Div([
                                            html.A("Lost password?", href='./forgot-password', className='small text-right')
                                        ])
                                    ], className='d-flex justify-content-between align-items-top mb-4')
                                ], className='form-group'),
                                html.Div([
                                    html.Button("Sign in", type='submit', className='btn btn-gray-800')
                                ], className='d-grid')
                            ], action='#', className='mt-4'),
                            html.Div([
                                html.Span("or login with", className='fw-normal')
                            ], className='mt-3 mb-4 text-center'),
                            html.Div([
                                html.A(FACEBOOK.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button', **{"aria-label": "facebook button"}),
                                html.A(TWITTER.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button', **{"aria-label": "twitter button"}),
                                html.A(GITHUB.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button', **{"aria-label": "github button"})
                            ], className='d-flex justify-content-center my-4'),
                            html.Div([
                                html.Span([
                                    "Not registered?",
                                    html.A("Create account", href='./sign-up', className='fw-bold')
                                ], className='fw-normal')
                            ], className='d-flex justify-content-center align-items-center mt-4')
                        ], className='card p-3 p-lg-4')
                    ], className='modal-body p-0')
                ], className='modal-content')
            ], className='modal-dialog modal-dialog-centered', role='document')
        ], className='modal fade', id='modal-form', role='dialog', **{"aria-labelledby": "modal-form", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')


def sign_out():
    return html.Div([
        # Button Modal
        html.Button("Sign Up", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-form-signup"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Button(type='button', className='btn-close ms-auto', **{"data-bs-dismiss": "modal", "aria-label": "Close"}),
                            html.Div([
                                html.H1("Create Account", className='mb-0 h4')
                            ], className='text-center text-md-center mb-4 mt-md-0'),
                            html.Form([
                                # Form
                                html.Div([
                                    html.Label("Your Email", htmlFor='email'),
                                    html.Div([
                                        html.Span(ICON.MAIL, className='input-group-text', id='basic-addon1'),
                                        dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', required='')
                                    ], className='input-group')
                                ], className='form-group mb-4'),
                                # End of Form
                                html.Div([
                                    # Form
                                    html.Div([
                                        html.Label("Your Password", htmlFor='password'),
                                        html.Div([
                                            html.Span(ICON.LOCK_CLOSED, className='input-group-text', id='basic-addon2'),
                                            dcc.Input(type='password', placeholder='Password', className='form-control', id='password', required='')
                                        ], className='input-group')
                                    ], className='form-group mb-4'),
                                    # End of Form
                                    # Form
                                    html.Div([
                                        html.Label("Confirm Password", htmlFor='confirm_password'),
                                        html.Div([
                                            html.Span(ICON.LOCK_CLOSED, className='input-group-text', id='basic-addon2'),
                                            dcc.Input(type='password', placeholder='Confirm Password', className='form-control', id='confirm_password', required='')
                                        ], className='input-group')
                                    ], className='form-group mb-4'),
                                    # End of Form
                                    html.Div([
                                        html.Div([
                                            dcc.Input(className='form-check-input', type='checkbox', value='', id='remember'),
                                            html.Label([
                                                "I agree to the",
                                                html.A("terms and conditions", href='#', className='fw-bold')
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
                                html.A(FACEBOOK.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button', **{"aria-label": "facebook button"}),
                                html.A(TWITTER.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button', **{"aria-label": "twitter button"}),
                                html.A(GITHUB.XXS, href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button', **{"aria-label": "github button"})
                            ], className='d-flex justify-content-center my-3'),
                            html.Div([
                                html.Span([
                                    "Already have an account?",
                                    html.A("Login here", href='./sign-in', className='fw-bold')
                                ], className='fw-normal')
                            ], className='d-flex justify-content-center align-items-center mt-4')
                        ], className='card p-3 p-lg-4')
                    ], className='modal-body p-0')
                ], className='modal-content')
            ], className='modal-dialog modal-dialog-centered', role='document')
        ], className='modal fade', id='modal-form-signup', role='dialog', **{"aria-labelledby": "modal-form-signup", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')


def achievement():
    return  html.Div([
        # Button Modal
        html.Button("Achievement", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-achievement"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Button(type='button', className='btn-close theme-settings-close fs-6 ms-auto', **{"data-bs-dismiss": "modal", "aria-label": "Close"}),
                    html.Div([
                        html.P("You just unlocked a new badge", className='lead mb-0 text-white')
                    ], className='modal-header mx-auto'),
                    html.Div([
                        html.Div([
                            html.Span(ICON.FIRE.LG, className='modal-icon display-1 text-white'),
                            html.H2("Author Level 5", className='h3 modal-title mb-3 text-white'),
                            html.P("One Thousand Dollars! Well done mate - heads are turning your way.", className='mb-4 text-white'),
                            html.Div([
                                html.Div(className='progress-bar bg-secondary', role='progressbar', style={'width': '50%'}, **{"aria-valuenow": "50", "aria-valuemin": "0", "aria-valuemax": "100"})
                            ], className='progress mb-0')
                        ], className='py-3 px-5 text-center')
                    ], className='modal-body pt-0'),
                    html.Div([
                        html.Button("Awesome!", type='button', className='btn btn-sm btn-white text-tertiary', **{"data-bs-dismiss": "modal"})
                    ], className='modal-footer d-flex justify-content-center pt-0 pb-3')
                ], className='modal-content')
            ], className='modal-dialog modal-tertiary modal-dialog-centered', role='document')
        ], className='modal fade', id='modal-achievement', role='dialog', **{"aria-labelledby": "modal-achievement", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')

def subscribe():
    return html.Div([
        # Button Modal
        html.Button("Subscribe", type='button', className='btn btn-block btn-gray-800 mb-3', **{"data-bs-toggle": "modal", "data-bs-target": "#modal-subscribe"}),
        # Modal Content
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Button(type='button', className='btn-close btn-close-white text-white', **{"data-bs-dismiss": "modal", "aria-label": "Close"})
                    ], className='modal-header'),
                    html.Div([
                        html.Span(ICON.MAIL_OPEN, className='modal-icon'),
                        html.H3("Join our 1,360,462 subscribers", className='modal-title mb-3'),
                        html.P("Get exclusive access to freebies, premium products and news.", className='mb-4 lead'),
                        html.Div([
                            html.Div([
                                dcc.Input(type='text', id='subscribe', className='me-sm-1 mb-sm-0 form-control form-control-lg', placeholder='example@company.com'),
                                html.Div([
                                    html.Button("Subscribe", type='submit', className='ms-2 btn large-form-btn btn-secondary')
                                ])
                            ], className='d-flex mb-3 justify-content-center')
                        ], className='form-group px-lg-5')
                    ], className='modal-body text-center py-3'),
                    html.Div([
                        html.P([
                            "We’ll never share your details with third parties.",
                            html.Br(className='visible-md'),
                            "View our",
                            html.A("Privacy Policy", href='#'),
                            "for more info."
                        ], className='text-white font-small')
                    ], className='modal-footer z-2 mx-auto text-center')
                ], className='modal-content bg-dark text-white')
            ], className='modal-dialog modal-tertiary modal-dialog-centered modal-lg', role='document')
        ], className='modal fade', id='modal-subscribe', role='dialog', **{"aria-labelledby": "modal-subscribe", "aria-hidden": "true"}),
        # End of Modal Content
    ], className='col-lg-4')


def modals():
    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        default(),
                        notification(),
                        sign_in(),
                        sign_out(),
                        achievement(),
                        subscribe()
                    ], className='row d-block mt-4')
                ], className='card-body')
            ], className='card border-0 shadow')
        ], className='col-12 mb-4')
    ], className='row')

layout = html.Main([
        topNavBar(),
        html.Div([
            breadCrumbs(["Components", "Modals"]),
            banner("Modals", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/modals/')
        ], className='py-4'),
        modals(),
        footer()
    ], className='content')
