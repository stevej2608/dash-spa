from dash import html, dcc
from dash_svg import Svg, Path
from dash_spa import register_page,  callback, NOUPDATE
from ..icons.hero import HOME
from ..common import breadCrumbs, banner, topNavBar, footer

register_page(__name__, path="/pages/components/typography", title="Dash/Flightdeck - Typography")

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


layout = html.Main([
        topNavBar(),
        html.Div([
            breadCrumbs(['components', 'Typography']),
            banner("Typography", 'https://themesberg.com/docs/volt-bootstrap-5-dashboard/foundation/typography/')
        ], className='py-4'),
        typography(),
        footer()
    ], className='content')
