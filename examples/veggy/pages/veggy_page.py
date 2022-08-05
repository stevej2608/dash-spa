from dash import html, dcc
from dash_spa import register_page, callback, NOUPDATE

from .veggy import productList, header, footer, modal

register_page(__name__, path='/', title="Veggy", short_name='Veggy')

layout = html.Main([
    html.Div([
        header(),
        productList(),
        footer(),
        modal()
    ], className='container')
])
