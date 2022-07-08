from dash import html, dcc
from dash_svg import Svg, Path
from dash_spa import register_page,  callback, NOUPDATE
from ..icons.hero import HOME_ICON
from ..common import sideBar, mobileNavBar, topNavBar, footer

register_page(__name__, path="/pages/components/modals.html", title="Dash/Flightdeck - Modals")

def breadCrumbs():
    return  html.Nav([
        html.Ol([
            html.Li([
                html.A([
                    HOME_ICON
                ], href='#')
            ], className='breadcrumb-item'),
            html.Li([
                html.A("Components", href='#')
            ], className='breadcrumb-item'),
            html.Li("Modals", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})


def banner():
    return html.Div([
        html.Div([
            html.H1("Modals", className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                html.I(className='far fa-question-circle me-1'),
                "Modal Docs"
            ], href='https://themesberg.com/docs/volt-bootstrap-5-dashboard/components/modals/', className='btn btn-outline-gray')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')

def modals():
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
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
                            ], className='col-lg-4'),
                            html.Div([
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
                                                    html.Span([
                                                        Svg([
                                                            Path(d='M8.707 7.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l2-2a1 1 0 00-1.414-1.414L11 7.586V3a1 1 0 10-2 0v4.586l-.293-.293z'),
                                                            Path(d='M3 5a2 2 0 012-2h1a1 1 0 010 2H5v7h2l1 2h4l1-2h2V5h-1a1 1 0 110-2h1a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5z')
                                                        ], className='icon icon-xl text-gray-200', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                                    ], className='modal-icon'),
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
                            ], className='col-lg-4'),
                            html.Div([
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
                                                                html.Span([
                                                                    Svg([
                                                                        Path(d='M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z'),
                                                                        Path(d='M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z')
                                                                    ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                                                ], className='input-group-text', id='basic-addon1'),
                                                                dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', required='')
                                                            ], className='input-group')
                                                        ], className='form-group mb-4'),
                                                        # End of Form
                                                        html.Div([
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
                                                            html.Div([
                                                                html.Div([
                                                                    dcc.Input(className='form-check-input', type='checkbox', value='', id='remember'),
                                                                    html.Label("Remember me", className='form-check-label mb-0', htmlFor='remember')
                                                                ], className='form-check'),
                                                                html.Div([
                                                                    html.A("Lost password?", href='./forgot-password.html', className='small text-right')
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
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z')
                                                            ], className='icon icon-xxs',  role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 320 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "facebook-f"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button', **{"aria-label": "facebook button"}),
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z')
                                                            ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 512 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "twitter"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button', **{"aria-label": "twitter button"}),
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z')
                                                            ], className='icon icon-xxs',  role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 496 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "github"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button', **{"aria-label": "github button"})
                                                    ], className='d-flex justify-content-center my-4'),
                                                    html.Div([
                                                        html.Span([
                                                            "Not registered?",
                                                            html.A("Create account", href='./sign-up.html', className='fw-bold')
                                                        ], className='fw-normal')
                                                    ], className='d-flex justify-content-center align-items-center mt-4')
                                                ], className='card p-3 p-lg-4')
                                            ], className='modal-body p-0')
                                        ], className='modal-content')
                                    ], className='modal-dialog modal-dialog-centered', role='document')
                                ], className='modal fade', id='modal-form', role='dialog', **{"aria-labelledby": "modal-form", "aria-hidden": "true"}),
                                # End of Modal Content
                            ], className='col-lg-4'),
                            html.Div([
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
                                                                html.Span([
                                                                    Svg([
                                                                        Path(d='M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z'),
                                                                        Path(d='M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z')
                                                                    ], className='icon icon-xs text-gray-600', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                                                ], className='input-group-text', id='basic-addon1'),
                                                                dcc.Input(type='email', className='form-control', placeholder='example@company.com', id='email', required='')
                                                            ], className='input-group')
                                                        ], className='form-group mb-4'),
                                                        # End of Form
                                                        html.Div([
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
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z')
                                                            ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 320 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "facebook-f"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button', **{"aria-label": "facebook button"}),
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z')
                                                            ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 512 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "twitter"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button', **{"aria-label": "twitter button"}),
                                                        html.A([
                                                            Svg([
                                                                Path(fill='currentColor', d='M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z')
                                                            ], className='icon icon-xxs',  role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 496 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "github"})
                                                        ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button', **{"aria-label": "github button"})
                                                    ], className='d-flex justify-content-center my-3'),
                                                    html.Div([
                                                        html.Span([
                                                            "Already have an account?",
                                                            html.A("Login here", href='./sign-in.html', className='fw-bold')
                                                        ], className='fw-normal')
                                                    ], className='d-flex justify-content-center align-items-center mt-4')
                                                ], className='card p-3 p-lg-4')
                                            ], className='modal-body p-0')
                                        ], className='modal-content')
                                    ], className='modal-dialog modal-dialog-centered', role='document')
                                ], className='modal fade', id='modal-form-signup', role='dialog', **{"aria-labelledby": "modal-form-signup", "aria-hidden": "true"}),
                                # End of Modal Content
                            ], className='col-lg-4'),
                            html.Div([
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
                                                    html.Span([
                                                        Svg([
                                                            Path(fillRule='evenodd', d='M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z', clipRule='evenodd')
                                                        ], className='icon icon-lg text-gray-200', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                                    ], className='modal-icon display-1 text-white'),
                                                    html.H2("Author Level 5", className='h3 modal-title mb-3 text-white'),
                                                    html.P("One Thousand Dollars! Well done mate - heads are turning your way.", className='mb-4 text-white'),
                                                    html.Div([
                                                        html.Div(className='progress-bar bg-secondary', role='progressbar', style='width: 50%', **{"aria-valuenow": "50", "aria-valuemin": "0", "aria-valuemax": "100"})
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
                            ], className='col-lg-4'),
                            html.Div([
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
                                                html.Span([
                                                    Svg([
                                                        Path(fillRule='evenodd', d='M2.94 6.412A2 2 0 002 8.108V16a2 2 0 002 2h12a2 2 0 002-2V8.108a2 2 0 00-.94-1.696l-6-3.75a2 2 0 00-2.12 0l-6 3.75zm2.615 2.423a1 1 0 10-1.11 1.664l5 3.333a1 1 0 001.11 0l5-3.333a1 1 0 00-1.11-1.664L10 11.798 5.555 8.835z', clipRule='evenodd')
                                                    ], className='icon icon-xl text-gray-200 mb-4', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg')
                                                ], className='modal-icon'),
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
                        ], className='row d-block mt-4')
                    ], className='card-body')
                ], className='card border-0 shadow')
            ], className='col-12 mb-4')
        ], className='row')

layout = html.Div([
        mobileNavBar(),
        sideBar(),
        html.Main([
            topNavBar(),
            html.Div([
                breadCrumbs(),
                banner()
            ], className='py-4'),
            modals(),
            footer()
        ], className='content')
    ])