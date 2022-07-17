from dash import html

from ..icons.hero import ICON

def cardFrame(content):
    return html.Div([
        html.Div([
            html.Div([
                html.Div(content, className='row d-block d-xl-flex align-items-center')
            ], className='card-body')
        ], className='card border-0 shadow')
    ], className='col-12 col-sm-6 col-xl-4 mb-4')



def customers():
    return cardFrame([
        html.Div([
            html.Div([
                ICON.PEOPLE
            ], className='icon-shape icon-shape-primary rounded me-4 me-sm-0'),
            html.Div([
                html.H2("Customers", className='h5'),
                html.H3("345,678", className='fw-extrabold mb-1')
            ], className='d-sm-none')
        ], className='col-12 col-xl-5 text-xl-center mb-3 mb-xl-0 d-flex align-items-center justify-content-xl-center'),
        html.Div([
            html.Div([
                html.H2("Customers", className='h6 text-gray-400 mb-0'),
                html.H3("345k", className='fw-extrabold mb-2')
            ], className='d-none d-sm-block'),
            html.Small([
                "Feb 1 - Apr 1,",
                ICON.GLOBE.ME1,
                "USA"
            ], className='d-flex align-items-center text-gray-500'),
            html.Div([
                html.Div([
                    "Since last month",
                    ICON.UP_ARROW.XS,
                    html.Span("22%", className='text-success fw-bolder')
                ])
            ], className='small d-flex mt-1')
        ], className='col-12 col-xl-7 px-xl-0')
    ])


def revenue():
    return cardFrame([
        html.Div([
            html.Div([
                ICON.BAG
            ], className='icon-shape icon-shape-secondary rounded me-4 me-sm-0'),
            html.Div([
                html.H2("Revenue", className='fw-extrabold h5'),
                html.H3("$43,594", className='mb-1')
            ], className='d-sm-none')
        ], className='col-12 col-xl-5 text-xl-center mb-3 mb-xl-0 d-flex align-items-center justify-content-xl-center'),
        html.Div([
            html.Div([
                html.H2("Revenue", className='h6 text-gray-400 mb-0'),
                html.H3("$43,594", className='fw-extrabold mb-2')
            ], className='d-none d-sm-block'),
            html.Small([
                "Feb 1 - Apr 1,",
                ICON.GLOBE.ME1,
                "GER"
            ], className='d-flex align-items-center text-gray-500'),
            html.Div([
                html.Div([
                    "Since last month",
                    ICON.DOWN_ARROW.XS,
                    html.Span("2%", className='text-danger fw-bolder')
                ])
            ], className='small d-flex mt-1')
        ], className='col-12 col-xl-7 px-xl-0')
    ])


def bounceRate():
    return cardFrame([
        html.Div([
            html.Div([
                ICON.CHART
            ], className='icon-shape icon-shape-tertiary rounded me-4 me-sm-0'),
            html.Div([
                html.H2("Bounce Rate", className='fw-extrabold h5'),
                html.H3("50.88%", className='mb-1')
            ], className='d-sm-none')
        ], className='col-12 col-xl-5 text-xl-center mb-3 mb-xl-0 d-flex align-items-center justify-content-xl-center'),
        html.Div([
            html.Div([
                html.H2("Bounce Rate", className='h6 text-gray-400 mb-0'),
                html.H3("50.88%", className='fw-extrabold mb-2')
            ], className='d-none d-sm-block'),
            html.Small("Feb 1 - Apr 1", className='text-gray-500'),
            html.Div([
                html.Div([
                    "Since last month",
                    ICON.UP_ARROW.XS,
                    html.Span("4%", className='text-success fw-bolder')
                ])
            ], className='small d-flex mt-1')
        ], className='col-12 col-xl-7 px-xl-0')
    ])
