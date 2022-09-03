import traceback
import dash_bootstrap_components as dbc
import dash_spa as spa
from dash import html
from dash_spa.components import Footer, NavBar, NavbarBrand, NavbarLink, NavbarDropdown
from dash_spa.exceptions import InvalidAccess
from dash_spa.logging import log
from dash_spa_admin import AdminNavbarComponent

from pages import NAVBAR_PAGES

CSS = """
    .body {
        display: flex;
        flex-direction: column;
        margin: 0;
        min-height: 100vh;
    }

    header, footer {
        flex-grow: 0;
    }

    footer {
        background-color: #dedede;
    }

    main {
        flex-grow: 1;
    }

    .navbar-brand {
        text-transform: none;
    }

"""

def default_container(page, layout,  **kwargs):
    """Default page content container. All pages are wrapped by this content unless
    registered with container=None or container='some_other_container

    Args:
        layout (Component or callable): layout to be wrapped

    Returns:
        layout wrapped by container markup
    """

    log.info("*************** default_container page=%s *********************", page['module'])

    items_dropdown = NavbarDropdown([
            dbc.DropdownMenuItem("Item 1"),
            dbc.DropdownMenuItem("Item 2"),
            dbc.DropdownMenuItem("Item 3"),
        ], "Items")

    try:

        NAV_BAR_ITEMS = {
            'brand' : NavbarBrand(' DashSPA','/'),
            'left' : [NavbarLink(path=path) for path in NAVBAR_PAGES] + [items_dropdown],
            'right' : AdminNavbarComponent()
        }

        navbar = NavBar(NAV_BAR_ITEMS)
        footer = Footer(f'DashSPA {spa.__version__}')

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
            html.Header([
                navbar.layout(),
                html.Br()
                ]),
            html.Main([
                html.Div([

                    html.Div([
                        html.Div(content, className="col-md-12"),
                        # html.Div([], className="col-md-2")
                    ], className='row')

                ], className='container d-flex flex-column flex-grow-1'),
            ], role='main', className='d-flex'),
            html.Footer(footer.layout(), className='footer mt-auto')
        ], className='body')

    except Exception:
        log.warning(traceback.format_exc())
        page = spa.page_for('pages.not_found_404')
        return page.layout()

spa.register_container(default_container)
spa.add_style(CSS)
