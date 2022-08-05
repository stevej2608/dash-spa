from dash import html, dcc

from .cart import cart
from .search import search

VEGGY_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1493547373/dummy-logo/Veggy.png'

def brand():
    return  html.Div([
        html.Img(className='logo', src=VEGGY_IMG, alt='Veggy Brand Logo')
    ], className='brand')

def header():
    return html.Header([
        html.Div([
            brand(),
            search(),
            cart(),
        ], className='container')
    ])