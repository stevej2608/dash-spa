import traceback
from dash import html
import dash_spa as spa
from dash_spa.exceptions import InvalidAccess
from dash_spa.logging import log

from .common import sideBar, mobileNavBar

#sidebar_instance = sideBar()

def default_container(page, layout,  **_kwargs):
    """Default page content container. All pages are wrapped by this content unless
    registered with container=None or container='some_other_container'

    Args:
        layout (Component or callable): layout to be wrapped

    Returns:
        layout wrapped by container markup
    """

    # log.info("*************** default_container page=%s *********************", page['module'])

    try:

        try:
            content = layout(**_kwargs) if callable(layout) else layout
        except InvalidAccess:

            # To force the user to the login page uncomment the following lines
            #
            # page = spa.page_for('dash_spa_admin.page')
            # content = page.layout()

            page = spa.page_for('pages.not_found_404')
            return page.layout()

        return html.Div([
            #mobileNavBar(),
            sideBar(),
            content
        ])

    except Exception:
        log.warning(traceback.format_exc())
        page = spa.page_for('pages.not_found_404')
        return page.layout()


spa.register_container(default_container)


def full_page_container(page, layout,  **kwargs):
    """Full page container"""

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
