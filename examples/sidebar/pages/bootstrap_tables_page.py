from dash import html
from dash_spa import register_page

from .common import jumbotron_content

layout = jumbotron_content('Bootstrap Tables', 'Page')

register_page(__name__, path="/pages/tables/bootstrap-tables", title="Dash/Flightdeck - Bootstrap Tables")
