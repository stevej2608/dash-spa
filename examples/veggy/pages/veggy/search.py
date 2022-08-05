from dash import html, dcc
from .context import CartContext

SEARCH_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1494756966/icons/search-green.png'
BACK_ARROW_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1494756030/icons/back.png'


def search():

    search_input = dcc.Input(type='search', placeholder='Search for Vegetables and Fruits', id='search', className='search-keyword')
    state = CartContext.getState()

    @CartContext.On(search_input.input.value)
    def input_cb(value):
        state.search_term = value

    return  html.Div([
        html.A([
            html.Img(src=SEARCH_IMG, alt='search')
        ], className='mobile-search', href='#'),
        html.Form([
            html.A([
                html.Img(src=BACK_ARROW_IMG, alt='back')
            ], className='back-button', href='#'),
            search_input,
            html.Button(className='search-button', type='submit')
        ], action='#', method='get', className='search-form')
    ], className='search')
