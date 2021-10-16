"""dash-spa - Dash Single Page Application (SPA) Framework"""

from .spa_components import SpaComponents
from .spa_form import SpaForm
from .spa import SinglePageApp
from .spa_blueprint import Blueprint
from .navbar import NavbarLink, NavbarBrand, Footer, NavbarBase
from .page_not_found import PageNotFound
from .admin import *
from holoniq.utils import log

from ._version import __version__ as pkg_version

__version__ = pkg_version
__author__ = 'Steve Jones <jonesst2608@gmail.com>'
__all__ = []
