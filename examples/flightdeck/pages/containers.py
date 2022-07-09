from dash import html
import dash_spa as spa
from dash_spa.exceptions import InvalidAccess

from .common import sideBar, mobileNavBar


def default_container(layout,  **kwargs):
    """Default page content container. All pages are wrapped by this content unless
    registered with container=None or container='some_other_container

    Args:
        layout (Component or callable): layout to be wrapped

    Returns:
        layout wrapped by container markup
    """

    try:
        content = layout(**kwargs) if callable(layout) else layout

        layout = html.Div([
            mobileNavBar(),
            sideBar(),
            content
        ])

    except InvalidAccess:

        # To force the user to the login page uncomment the following lines
        #
        # page = spa.page_for('dash_spa_admin.page')
        # content = page.layout()

        page = spa.page_for('pages.not_found_404')
        layout = page.layout()

    return layout


spa.register_container(default_container)


def full_page_container(layout,  **kwargs):
    """Default page content container. All pages are wrapped by this content unless
    registered with container=None or container='some_other_container

    Args:
        layout (Component or callable): layout to be wrapped

    Returns:
        layout wrapped by container markup
    """


    try:
        content = layout(**kwargs) if callable(layout) else layout
    except InvalidAccess:

        # To force the user to the login page uncomment the following lines
        #
        # page = spa.page_for('dash_spa_admin.page')
        # content = page.layout()

        page = spa.page_for('pages.not_found_404')
        content = page.layout()

    return content

spa.register_container(full_page_container, name='full_page')
