from dash import html

from dash_spa import register_page

register_page(__name__, path="/pages/500", title="Dash - 500", container=None)

layout = html.Div([
        html.Div([
            html.H1("500", className='display-1 fw-bold'),
            html.P([
                html.Span("Server Error! ", className='text-danger'),
                "Something has gone seriously wrong.",
            ], className='fs-3'),
            html.A("Go Home", href='/', className='btn btn-secondary')
        ], className='text-center')
    ], className='d-flex align-items-center justify-content-center vh-100')