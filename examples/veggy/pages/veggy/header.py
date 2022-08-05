from dash import html, dcc

BAG_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1493548928/icons/bag.png'
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

def cart_info(items, total):
    return  html.Div([
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td("No. of items"),
                    html.Td(":"),
                    html.Td([
                        html.Strong(items)
                    ])
                ]),
                html.Tr([
                    html.Td("Sub Total"),
                    html.Td(":"),
                    html.Td([
                        html.Strong(total)
                    ])
                ])
            ])
        ])
    ], className='cart-info')

def cart_preview():
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src=BAG_IMG, alt='empty-cart'),
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

def cart():
    return  html.Div([
        cart_info(0, 0),
        html.A(html.Img(className='', src=BAG_IMG, alt='Cart'), className='cart-icon', href='#'),
        cart_preview()
    ], className='cart')


def header():
    return html.Header([
        html.Div([
            brand(),
            search(),
            cart(),
        ], className='container')
    ])