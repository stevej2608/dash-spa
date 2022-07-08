from dash import html, dcc
from dash_svg import Svg, Path
from dash_spa import register_page,  callback, NOUPDATE
from ..icons.hero import HOME_ICON
from ..common import sideBar, mobileNavBar, topNavBar, footer

register_page(__name__, path="/pages/components/typography.html", title="Dash/Flightdeck - Typography")

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
            html.Li("Typography", className='breadcrumb-item active', **{"aria-current": "page"})
        ], className='breadcrumb breadcrumb-dark breadcrumb-transparent')
    ], className='d-none d-md-inline-block', **{"aria-label": "breadcrumb"})


def banner():
    return html.Div([
        html.Div([
            html.H1("Typography", className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                html.I(className='far fa-question-circle me-1'),
                "Typography Docs"
            ], href='https://themesberg.com/docs/volt-bootstrap-5-dashboard/foundation/typography/', className='btn btn-outline-gray')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')

def typography():
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H2("Headings", className='h5 mb-3'),
                                html.H1("h1. Themesberg heading"),
                                html.H2("h2. Themesberg heading"),
                                html.H3("h3. Themesberg heading"),
                                html.H4("h4. Themesberg heading"),
                                html.H5("h5. Themesberg heading"),
                                html.H6("h6. Themesberg heading")
                            ], className='col-12 col-md-6'),
                            html.Div([
                                html.H2("Display Headings", className='h5 mb-3'),
                                html.H1("Display 1", className='display-1'),
                                html.H1("Display 2", className='display-2'),
                                html.H1("Display 3", className='display-3'),
                                html.H1("Display 4", className='display-4')
                            ], className='col-12 col-md-6')
                        ], className='row mb-4 mb-lg-5'),
                        # Title
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.H2("Paragraphs", className='h5 mb-3')
                                ], className='mb-5')
                            ], className='col-md-4')
                        ], className='row'),
                        # End of Title
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span("Simple paragraph", className='h6 fw-bold')
                                ], className='mb-3'),
                                html.P("Start your development with a Pixel Design System for Bootstrap 4. Themesberg makes beautiful products to help people with creative ideas succeed.Our company empowers millions of people.")
                            ], className='col-md-6'),
                            html.Div([
                                html.Div([
                                    html.Span("Lead paragraph", className='h6 fw-bold')
                                ], className='mt-5 mb-3 mt-sm-0'),
                                html.P("Start your development with a Pixel Design System for Bootstrap 4.Themesberg makes beautiful products to help people with creative ideas succeed.Our company empowers millions of people.", className='lead')
                            ], className='col-md-6')
                        ], className='row mb-4 mb-lg-5'),
                        html.Div([
                            html.Div([
                                html.Small("Dark text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-dark mb-0')
                            ], className='col-sm-10')
                        ], className='row mt-4 mb-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Primary text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-primary mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Secondary text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-secondary mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Tertiary text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-tertiary mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Info text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-info mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Danger text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-danger mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        html.Div([
                            html.Div([
                                html.Small("Success text", className='text-uppercase text-muted')
                            ], className='col-sm-2'),
                            html.Div([
                                html.P("Design is not just what it looks like and feels like. Design is how it works.", className='text-success mb-0')
                            ], className='col-sm-10')
                        ], className='row py-3 align-items-center'),
                        # Title
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span("Blockquote", className='h6')
                                ], className='mt-6 mb-5')
                            ], className='col-md-4')
                        ], className='row'),
                        # End of Title
                        html.Div([
                            html.Div([
                                html.Blockquote([
                                    "Themesberg makes beautiful products to help people with creative ideas succeed. Our company empowers millions of people.",
                                    html.Footer("Zoltan Szőgyényi", className='blockquote-footer mt-3 text-primary')
                                ], className='blockquote text-center')
                            ], className='col-md-8')
                        ], className='row'),
                        # Title
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span("Lists", className='h6')
                                ], className='mt-6 mb-5')
                            ], className='col-md-4')
                        ], className='row'),
                        # End of Title
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Span("Unordered", className='h6')
                                ], className='mb-3'),
                                html.Ul([
                                    html.Li("Minutes of the last meeting"),
                                    html.Li("Do we need yet more meetings?"),
                                    html.Li([
                                        "Any other business",
                                        html.Ul([
                                            html.Li("Programming"),
                                            html.Li("Web Design"),
                                            html.Li("Database")
                                        ])
                                    ]),
                                    html.Li("Something funny")
                                ])
                            ], className='col-md-6'),
                            html.Div([
                                html.Div([
                                    html.Span("Ordered", className='h6 fw-bold')
                                ], className='mt-5 mb-3 mt-sm-0'),
                                html.Ol([
                                    html.Li("Minutes of the last meeting"),
                                    html.Li("Do we need yet more meetings?"),
                                    html.Li([
                                        "Any other business",
                                        html.Ol([
                                            html.Li("Programming"),
                                            html.Li("Web Design"),
                                            html.Li("Database")
                                        ])
                                    ]),
                                    html.Li("Something funny")
                                ])
                            ], className='col-md-6')
                        ], className='row')
                    ], className='card-body')
                ], className='card border-0 shadow components-section')
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
            typography(),
            footer()
        ], className='content')
    ])