from dash import html
from dash_spa import register_page
from .common import jumbotron_content

register_page(__name__, path='/', title='Welcome')

layout = jumbotron_content("DashSPA Welcomes", 'Guest')

