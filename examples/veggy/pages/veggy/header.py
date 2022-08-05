from dash import html, dcc

from .cart import cart

VEGGY_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1493547373/dummy-logo/Veggy.png'
SEARCH_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1494756966/icons/search-green.png'
BACK_ARROW_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1494756030/icons/back.png'

def search():
    return  html.Div([
        html.A([
            html.Img(src=SEARCH_IMG, alt='search')
        ], className='mobile-search', href='#'),
        html.Form([
            html.A([
                html.Img(src=BACK_ARROW_IMG, alt='back')
            ], className='back-button', href='#'),
            dcc.Input(type='search', placeholder='Search for Vegetables and Fruits', className='search-keyword'),
            html.Button(className='search-button', type='submit')
        ], action='#', method='get', className='search-form')
    ], className='search')


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