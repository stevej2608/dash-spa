from unicodedata import category
import pandas as pd
from dash import html, dcc

try:
    df = pd.read_json('https://res.cloudinary.com/sivadass/raw/upload/v1535817394/json/products.json')
except Exception:
    print("Unable to read 'product.json' from cloudinary, no internet connection?")
    exit(0)


def ProductCard(index, data: list):
    id, name, price, image, category = data.values()
    return html.Div([
        html.Div([
            html.Img(src=image, alt=name)
        ], className='product-image'),
        html.H4(name, className='product-name'),
        html.P(price, className='product-price'),
        html.Div([
            html.A("–", href='#', className='decrement'),
            dcc.Input(type='number', className='quantity', value='1'),
            html.A("+", href='#', className='increment')
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