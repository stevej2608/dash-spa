"""dash-spa - Dash Single Page Application (SPA) Framework"""

from .spa_dependency import SpaDependency
from .spa_components import SpaComponents
from .spa import SinglePageApp
from .spa_blueprint import Blueprint
from .navbar import NavbarLink, NavbarBrand, Footer, NavbarBase
from .page_not_found import PageNotFound
from .admin import *
from holoniq.utils import log

__version__ = '0.0.3'
__author__ = 'Steve Jones <jonesst2608@gmail.com>'
__all__ = []
