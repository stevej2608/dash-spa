import traceback
from dash import html
import dash_spa as spa
from pages import NAVBAR_PAGES
from dash_spa.logging import log
from dash_spa_admin import AdminNavbarComponent
from dash_spa.exceptions import InvalidAccess

def default_container(page, layout,  **kwargs):
    """Default page content container. All pages are wrapped by this content unless
    registered with container=None or container='some_other_container

    Args:
        layout (Component or callable): layout to be wrapped

    Returns:
        layout wrapped by container markup
    """

    try:

        NAV_BAR_ITEMS = {
            'brand' : spa.NavbarBrand(' Dash/SPA','/'),
            'left' : [spa.NavbarLink(path=path) for path in NAVBAR_PAGES],
            'right' : AdminNavbarComponent()
        }

        navbar = spa.NavBar(NAV_BAR_ITEMS)
        footer = spa.Footer(f'Dash/SPA {spa.__version__}')

        try:
            content = layout(**kwargs) if callable(layout) else layout
        except InvalidAccess:

            # To force the user to the login page uncomment the following lines
            #
            # page = spa.page_for('dash_spa_admin.page')
            # content = page.layout()

            page = spa.page_for('pages.not_found_404')
            return page.layout()

        return html.Div([
            navbar.layout(),
            html.Br(),
            html.Main([
                html.Div([
                    html.Div(content, className="col-md-10"),
                    html.Div([], className="col-md-2")
                ], className='row')
            ], className='content'),
            html.Div(id='null'),
            html.Div(footer.layout())
        ])
    except Exception:
        log.warn(traceback.format_exc())
        page = spa.page_for('pages.not_found_404')
        return page.layout()


#spa.register_container(default_container)
