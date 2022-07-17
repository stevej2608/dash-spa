from dash import html, dcc

from ..icons.hero import ICON

def settingsPopupPanel():
    return html.Div([
        html.Div([
            html.Button(type='button', className='btn-close theme-settings-close'),
            html.Div([
                html.P([
                    "Open source",
                    html.Span("💛", role='img', **{"aria-label": "gratitude"})
                ], className='m-0 mb-1 me-4 fs-7'),
                dcc.Link("Star", className='github-button', href='https://github.com/themesberg/volt-bootstrap-5-dashboard', **{"data-color-scheme": "no-preference: dark; light: light; dark: light;", "data-icon": "octicon-star", "data-size": "large", "data-show-count": "true", "aria-label": "Star themesberg/volt-bootstrap-5-dashboard on GitHub"})
            ], className='d-flex justify-content-between align-items-center mb-3'),
            dcc.Link([
                "Download",
                ICON.DOWNLOAD
            ], href='https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard', target='_blank', className='btn btn-secondary d-inline-flex align-items-center justify-content-center mb-3 w-100'),
            html.P("Available in the following technologies:", className='fs-7 text-gray-300 text-center'),
            html.Div([
                dcc.Link([
                    html.Img(src='../assets/img/technologies/bootstrap-5-logo.svg', className='image image-xs')
                ], className='me-3', href='https://themesberg.com/product/admin-dashboard/volt-bootstrap-5-dashboard', target='_blank'),
                dcc.Link([
                    html.Img(src='../assets/img/technologies/react-logo.svg', className='image image-xs')
                ], href='https://demo.themesberg.com/volt-react-dashboard/#/', target='_blank')
            ], className='d-flex justify-content-center')
        ], className='card-body bg-gray-800 text-white pt-4')
    ], className='theme-settings card bg-gray-800 pt-2 collapse', id='theme-settings')


def settingsPopupButton():
    return html.Div([
        html.Div([
            html.Span([
                ICON.VIEW_GRID,
                "Settings"
            ], className='fw-bold d-inline-flex align-items-center h6')
        ], className='card-body bg-gray-800 text-white rounded-top p-3 py-2')
    ], className='card theme-settings bg-gray-800 theme-settings-expand', id='theme-settings-expand')
