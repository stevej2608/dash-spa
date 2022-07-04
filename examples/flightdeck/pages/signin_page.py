from dash import html, dcc
from dash_svg import Svg, Path
from dash_spa import register_page
from .components import background_img

register_page(__name__, path="/pages/sign-in.html", title="Dash/Flightdeck - Sign in")

layout = html.Div([
    # NOTICE: You can use the _analytics.html partial to include production code specific code & trackers
    html.Main([
        # Section
        html.Section([
            html.Div([
                html.P([
                    dcc.Link([
                        Svg([
                            Path(fillRule='evenodd', d='M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z', clipRule='evenodd')
                        ], className='icon icon-xs me-2', fill='currentColor', viewBox='0 0 20 20', xmlns='http://www.w3.org/2000/svg'),
                        "Back to homepage"
                    ], href='dashboard.html', className='d-flex align-items-center justify-content-center')
                ], className='text-center'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H1("Sign in to our platform", className='mb-0 h3')
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
                                            dcc.Link("Lost password?", href='./forgot-password.html', className='small text-right')
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
                                dcc.Link([
                                    Svg([
                                        Path(fill='currentColor', d='M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06h40.42V6.26S260.43 0 225.36 0c-73.22 0-121.08 44.38-121.08 124.72v70.62H22.89V288h81.39v224h100.17V288z')
                                    ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 320 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "facebook-f"})
                                ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='facebook button'),
                                dcc.Link([
                                    Svg([
                                        Path(fill='currentColor', d='M459.37 151.716c.325 4.548.325 9.097.325 13.645 0 138.72-105.583 298.558-298.558 298.558-59.452 0-114.68-17.219-161.137-47.106 8.447.974 16.568 1.299 25.34 1.299 49.055 0 94.213-16.568 130.274-44.832-46.132-.975-84.792-31.188-98.112-72.772 6.498.974 12.995 1.624 19.818 1.624 9.421 0 18.843-1.3 27.614-3.573-48.081-9.747-84.143-51.98-84.143-102.985v-1.299c13.969 7.797 30.214 12.67 47.431 13.319-28.264-18.843-46.781-51.005-46.781-87.391 0-19.492 5.197-37.36 14.294-52.954 51.655 63.675 129.3 105.258 216.365 109.807-1.624-7.797-2.599-15.918-2.599-24.04 0-57.828 46.782-104.934 104.934-104.934 30.213 0 57.502 12.67 76.67 33.137 23.715-4.548 46.456-13.32 66.599-25.34-7.798 24.366-24.366 44.833-46.132 57.827 21.117-2.273 41.584-8.122 60.426-16.243-14.292 20.791-32.161 39.308-52.628 54.253z')
                                    ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 512 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "twitter"})
                                ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500 me-2', title='twitter button'),
                                dcc.Link([
                                    Svg([
                                        Path(fill='currentColor', d='M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z')
                                    ], className='icon icon-xxs', role='img', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 496 512', **{"aria-hidden": "true", "data-prefix": "fab", "data-icon": "github"})
                                ], href='#', className='btn btn-icon-only btn-pill btn-outline-gray-500', title='github button')
                            ], className='d-flex justify-content-center my-4'),
                            html.Div([
                                html.Span([
                                    "Not registered?",
                                    dcc.Link("Create account", href='./sign-up.html', className='fw-bold')
                                ], className='fw-normal')
                            ], className='d-flex justify-content-center align-items-center mt-4')
                        ], className='bg-white shadow border-0 rounded border-light p-4 p-lg-5 w-100 fmxw-500')
                    ], className='col-12 d-flex align-items-center justify-content-center')
                ], className='row justify-content-center form-bg-image', style=background_img("/assets/img/illustrations/signin.svg"))
            ], className='container')
        ], className='vh-lg-100 mt-5 mt-lg-0 bg-soft d-flex align-items-center')
    ])
])
