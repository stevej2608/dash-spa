from dash import html, dcc

class PageNotFound:

    def layout(self, spa):
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1('Oops!'),
                        html.H2('404 Not Found'),
                        html.Div('Sorry, an error has occurred, Requested page not found!', className='error-details'),
                        html.Div([

                            dcc.Link([
                                html.Span(className='fa fa-home'),
                                ' Take Me Home'
                            ], href='/', className='btn btn-secondary btn-lg'),

                            dcc.Link([
                                html.Span(className='fa fa-envelope'),
                                ' Contact Support'
                            ], href='/support', className='btn btn-secondary btn-lg'),

                        ], className='error-actions')
                    ], className='error-template')
                ], className='col-md-12')
            ], className='row')
        ], className='container')