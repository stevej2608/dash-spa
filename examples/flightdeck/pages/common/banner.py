from dash import html

def banner(title, link):
    return html.Div([
        html.Div([
            html.H1(title, className='h4'),
            html.P("Dozens of reusable components built to provide buttons, alerts, popovers, and more.", className='mb-0')
        ], className='mb-3 mb-lg-0'),
        html.Div([
            html.A([
                html.I(className='far fa-question-circle me-1'),
                f"{title} Docs"
            ], href=link, className='btn btn-outline-gray')
        ])
    ], className='d-flex justify-content-between w-100 flex-wrap')