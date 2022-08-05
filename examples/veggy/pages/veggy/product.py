from unicodedata import category
import pandas as pd
from dash import html, dcc
from dash_spa import prefix

from .cart import CartContext, TCartItem

try:
    df = pd.read_json('https://res.cloudinary.com/sivadass/raw/upload/v1535817394/json/products.json')
except Exception:
    print("Unable to read 'product.json' from cloudinary, no internet connection?")
    exit(0)


def ProductCard(index, data: list):

    pid = prefix(f'product_card_{index}')

    id, name, price, image, category = data.values()

    add_btn = html.A("+", href='#', className='increment', id=pid('add'))
    remove_btn = html.A("–", href='#', className='decrement', id=pid('remove'))
    input_number = dcc.Input(type='number', className='quantity', value='1', id=pid('input'))

    state = CartContext.getState()

    def update_item(count):
        nonlocal state, id

        if state.items is None:
            state.items = []

        for item in state.items:
            if item.id == id:
                item.count += count
                return

        new_item = TCartItem(id, count)
        state.items.append(new_item)


    @CartContext.On(add_btn.input.n_clicks)
    def add_cb(clicks):
        update_item(1)

    @CartContext.On(remove_btn.input.n_clicks)
    def add_cb(clicks):
        update_item(-1)

    @CartContext.On(input_number.input.value)
    def add_cb(value):
        update_item(value)


    return html.Div([
        html.Div([
            html.Img(src=image, alt=name)
        ], className='product-image'),
        html.H4(name, className='product-name'),
        html.P(price, className='product-price'),
        html.Div([
            add_btn,
            input_number,
            remove_btn
        ], className='stepper-input'),
        html.Div([
            html.Button("ADD TO CART", className='', type='button')
        ], className='product-action')
    ], className='product')


def productList():
    product_data = df.to_dict('records')
    products = [ProductCard(index, data) for index, data in enumerate(product_data)]
    return html.Div([
            html.Div(products, className='products')
        ], className='products-wrapper')