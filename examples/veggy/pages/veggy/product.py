import pandas as pd
from dash import html
from dash_spa import prefix, callback, isTriggered, copy_factory

from .cart import CartContext, TCartItem
from .stepper_input import StepperInput

try:
    df = pd.read_json('https://res.cloudinary.com/sivadass/raw/upload/v1535817394/json/products.json')
except Exception:
    print("Unable to read 'product.json' from cloudinary, no internet connection?")
    exit(0)


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
            value = int(value)
            if state.items is None:
                state.items = []

            for item in state.items:
                if item.id == id:
                    item.count += value
                    return

            new_item = TCartItem(id, value, price, name, image)
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