from dash import html
from dash_spa import register_page

from .common import jumbotron_content

layout = jumbotron_content('Transactions', 'Page')

page = register_page(__name__, path="/pages/transactions", title="Dash/Flightdeck - Transactions")

