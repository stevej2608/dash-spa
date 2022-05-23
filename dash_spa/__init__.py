"""dash-pages-spa - Dash Pages SPA Framework"""

__version__ = '1.0.1'
__author__ = 'Steve Jones <jonesst2608@gmail.com>'
__all__ = []

from dash.exceptions import PreventUpdate
from .spa_config import config
from dash_prefix import prefix, match, isTriggered, trigger_index, NOUPDATE, copy_factory, component_id
from .spa_pages import register_page, page_container, page_container_append, spa_plugin, location, url_for, page_for, get_page, register_container
from .spa_pages import add_style
from .components.navbar import NavBar, NavbarBrand, NavbarLink
from .components.footer import  Footer
from .spa_form import SpaForm
from .spa_current_user import current_user
from .decorators import login_required

from dash_spa import themes
