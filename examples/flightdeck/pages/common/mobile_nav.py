from dash import html, dcc

from ..icons.hero import CROSS_ICON

def mobileNavBar():
    """ Mobile only navbar - Volt logo & burger button """
    return html.Nav([
        html.A([
            html.Img(className='navbar-brand-dark', src='../../assets/img/brand/light.svg', alt='Volt logo'),
            html.Img(className='navbar-brand-light', src='../../assets/img/brand/dark.svg', alt='Volt logo')
        ], className='navbar-brand me-lg-5', href='../../index'),
        html.Div([
            html.Button([

                # Burger button

                html.Span(className='navbar-toggler-icon')

            ], className='navbar-toggler d-lg-none collapsed', type='button', **{"data-bs-toggle": "collapse", "data-bs-target": "#sidebarMenu", "aria-controls": "sidebarMenu", "aria-expanded": "false", "aria-label": "Toggle navigation"})
        ], className='d-flex align-items-center')
    ], className='navbar navbar-dark navbar-theme-primary px-4 col-12 d-lg-none')


def mobileSidebarHeader():
    """ Mobile only sidebar header"""
    return html.Div([
        html.Div([
            # Snip avatar
            html.Div([
                # Snip Hi, Jane
                html.A([
                    html.Img(className='icon icon-sm', src='../../assets/img/icons/sign_out.svg', height='20', width='20', alt='upgrade'),
                    "Sign Out"
                ], href='../../pages/examples/sign-in', className='btn btn-secondary btn-sm d-inline-flex align-items-center')
            ], className='d-block')
        ], className='d-flex align-items-center'),

        # Sidebar close [X] icon

        html.Div([
            html.A([
                CROSS_ICON,
            ], href='#sidebarMenu', **{"data-bs-toggle": "collapse", "data-bs-target": "#sidebarMenu", "aria-controls": "sidebarMenu", "aria-expanded": "true", "aria-label": "Toggle navigation"})
        ], className='collapse-close d-md-none')

    ], className='user-card d-flex d-md-none align-items-center justify-content-between justify-content-md-center pb-4')
