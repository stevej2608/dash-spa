from dash import html, dcc
from dash_spa import register_page, callback, NOUPDATE

from .veggy.product import productList

register_page(__name__, path='/', title="Veggy", short_name='Veggy')

WS = "\n"

layout = html.Main([
    html.Div([
        html.Header([
            html.Div([
                html.Div([
                    html.Img(className='logo', src='https://res.cloudinary.com/sivadass/image/upload/v1493547373/dummy-logo/Veggy.png', alt='Veggy Brand Logo')
                ], className='brand'),
                html.Div([
                    html.A([
                        html.Img(src='https://res.cloudinary.com/sivadass/image/upload/v1494756966/icons/search-green.png', alt='search')
                    ], className='mobile-search', href='#'),
                    html.Form([
                        html.A([
                            html.Img(src='https://res.cloudinary.com/sivadass/image/upload/v1494756030/icons/back.png', alt='back')
                        ], className='back-button', href='#'),
                        dcc.Input(type='search', placeholder='Search for Vegetables and Fruits', className='search-keyword'),
                        html.Button(className='search-button', type='submit')
                    ], action='#', method='get', className='search-form')
                ], className='search'),
                html.Div([
                    html.Div([
                        html.Table([
                            html.Tbody([
                                html.Tr([
                                    html.Td("No. of items"),
                                    html.Td(":"),
                                    html.Td([
                                        html.Strong("0")
                                    ])
                                ]),
                                html.Tr([
                                    html.Td("Sub Total"),
                                    html.Td(":"),
                                    html.Td([
                                        html.Strong("0")
                                    ])
                                ])
                            ])
                        ])
                    ], className='cart-info'),
                    html.A([
                        html.Img(className='', src='https://res.cloudinary.com/sivadass/image/upload/v1493548928/icons/bag.png', alt='Cart')
                    ], className='cart-icon', href='#'),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Img(src='https://res.cloudinary.com/sivadass/image/upload/v1495427934/icons/empty-cart.png', alt='empty-cart'),
                                    html.H2("You cart is empty!")
                                ], className='empty-cart')
                            ], style='position: absolute; inset: 0px; overflow: scroll; margin-right: -17px; margin-bottom: -17px;'),
                            html.Div([
                                html.Div(style='position: relative; display: block; height: 100%; cursor: pointer; border-radius: inherit; background-color: rgba(0, 0, 0, 0.2); width: 0px;')
                            ], style='position: absolute; height: 6px; right: 2px; bottom: 2px; left: 2px; border-radius: 3px;'),
                            html.Div([
                                html.Div(style='position: relative; display: block; width: 100%; cursor: pointer; border-radius: inherit; background-color: rgba(0, 0, 0, 0.2); height: 0px;')
                            ], style='position: absolute; width: 6px; right: 2px; bottom: 2px; top: 2px; border-radius: 3px;')
                        ], style='position: relative; overflow: hidden; width: 360px; height: 320px;'),
                        html.Div([
                            html.Button("PROCEED TO CHECKOUT", type='button', className='disabled')
                        ], className='action-block')
                    ], className='cart-preview')
                ], className='cart')
            ], className='container')
        ]),

        productList(),

        html.Footer([
            html.P([
                html.A("View Source on Github", href='https://github.com/sivadass/react-shopping-cart', target='_blank'),
                html.Span("/"),
                html.A("Need any help?", href='mailto:contact@sivadass.in', target='_blank'),
                html.Span("/"),
                html.A("Say Hi on Twitter", href='https://twitter.com/NSivadass', target='_blank'),
                html.Span("/"),
                html.A("Read My Blog", href='https://sivadass.in', target='_blank')
            ], className='footer-links'),
            html.P(["© 2017", WS, html.Strong("Veggy"), WS, "- Organic Green Store" ])
        ]),
        html.Div([
            html.Div([
                html.Button("×", type='button', className='close'),
                html.Div([
                    html.Div([
                        html.Img()
                    ], className='quick-view-image'),
                    html.Div([
                        html.Span(className='product-name'),
                        html.Span(className='product-price')
                    ], className='quick-view-details')
                ], className='quick-view')
            ], className='modal')
        ], className='modal-wrapper')
    ], className='container')
])
