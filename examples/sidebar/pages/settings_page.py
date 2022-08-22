from dash import html
from dash_spa import register_page

from .common import jumbotron_content

layout = jumbotron_content('Settings', 'Page')

register_page(__name__, path="/pages/settings", title="Dash/Flightdeck - Settings")
