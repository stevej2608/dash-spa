from dash import html, dcc

def footer():
    return  html.Footer([
        html.Div([
            html.Div([
                html.P([
                    "© 2019-",
                    html.Span(className='current-year'),
                    dcc.Link("Themesberg", className='text-primary fw-normal', href='https://themesberg.com', target='_blank')
                ], className='mb-0 text-center text-lg-start')
            ], className='col-12 col-md-4 col-xl-6 mb-4 mb-md-0'),
            html.Div([
                # List
                html.Ul([
                    html.Li([
                        dcc.Link("About", href='https://themesberg.com/about')
                    ], className='list-inline-item px-0 px-sm-2'),
                    html.Li([
                        dcc.Link("Themes", href='https://themesberg.com/themes')
                    ], className='list-inline-item px-0 px-sm-2'),
                    html.Li([
                        dcc.Link("Blog", href='https://themesberg.com/blog')
                    ], className='list-inline-item px-0 px-sm-2'),
                    html.Li([
                        dcc.Link("Contact", href='https://themesberg.com/contact')
                    ], className='list-inline-item px-0 px-sm-2')
                ], className='list-inline list-group-flush list-group-borderless text-md-end mb-0')
            ], className='col-12 col-md-8 col-xl-6 text-center text-lg-start')
        ], className='row')
    ], className='bg-white rounded shadow p-5 mb-4 mt-4')
