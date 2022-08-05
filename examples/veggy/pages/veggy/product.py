from unicodedata import category
import pandas as pd
from dash import html, dcc
from dash_spa import prefix, callback, isTriggered, copy_factory

from .cart import CartContext, TCartItem

try:
    df = pd.read_json('https://res.cloudinary.com/sivadass/raw/upload/v1535817394/json/products.json')
except Exception:
    print("Unable to read 'product.json' from cloudinary, no internet connection?")
    exit(0)


class StepperInput(html.Div):

    def __init__(self, id):
        pid = prefix(id)
        add_btn = html.A("+", href='#', className='increment', id=pid('add'))
        remove_btn = html.A("–", href='#', className='decrement', id=pid('remove'))
        input_number = dcc.Input(type='number', className='quantity', value='1', id=pid('input'))

        @callback(input_number.output.value,
                  add_btn.input.n_clicks,
                  remove_btn.input.n_clicks,
                  input_number.state.value,
                  prevent_initial_call=True)
        def add_cb(add_clicks, remove_clicks, value):
            try:
                count = int(value)
                if isTriggered(add_btn.input.n_clicks):
                    count += 1
                elif isTriggered(remove_btn.input.n_clicks):
                    if count > 1: count -= 1
                return str(count)
            except Exception:
                return value

        super().__init__([remove_btn, input_number, add_btn], className='stepper-input')
        copy_factory(input_number, self)


def ProductCard(index, data: list):

    pid = prefix(f'product_card_{index}')

    id, name, price, image, category = data.values()

    state = CartContext.getState()

    stepper = StepperInput(id=pid('stepper'))
    add_btn = html.Button("ADD TO CART", className='', type='button', id=pid('add_btn'))

    @CartContext.On(add_btn.input.n_clicks, stepper.state.value)
    def update_cb(clicks, value):
        nonlocal state, id
        try:
            if state.items is None:
                state.items = []

            for item in state.items:
                if item.id == id:
                    item.count += value
                    return

            new_item = TCartItem(id, value, price)
            state.items.append(new_item)
        except Exception:
            pass

    return html.Div([
        html.Div([
            html.Img(src=image, alt=name)
        ], className='product-image'),
        html.H4(name, className='product-name'),
        html.P(price, className='product-price'),
        stepper,
        html.Div(add_btn, className='product-action')
    ], className='product')


def productList():
    product_data = df.to_dict('records')
    products = [ProductCard(index, data) for index, data in enumerate(product_data)]
    return html.Div([
            html.Div(products, className='products')
        ], className='products-wrapper')