from dash import html

from dash_spa import register_page

register_page(__name__, path="/pages/404", title="Dash - 404", container=None)

layout = html.Div([
        html.Div([
            html.H1("404", className='display-1 fw-bold'),
            html.P([
                html.Span("Opps! ", className='text-danger'),
                "Page not found."
            ], className='fs-3'),
            html.P("The page you're looking for doesn't exist.", className='lead'),
            html.A("Go Home", href='/', className='btn btn-secondary')
        ], className='text-center')
    ], className='d-flex align-items-center justify-content-center vh-100')
