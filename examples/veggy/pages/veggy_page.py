from dash import html
from dash_spa import register_page

from .veggy import productList, header, footer, modal, CartContext

register_page(__name__, path='/', title="Veggy", short_name='Veggy')

@CartContext.Provider()
def layout():
    return html.Main([
    html.Div([
        header(),
        productList(),
        footer(),
        modal()
    ], className='container')
])
