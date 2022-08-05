from dash import html
from dash_spa import prefix
from dash_spa.components.dropdown_aio import DropdownAIO

from .context import TCartItem, TCartState, CartContext

BAG_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1493548928/icons/bag.png'
EMPTY_CART = 'https://res.cloudinary.com/sivadass/image/upload/v1495427934/icons/empty-cart.png'


STYLE = {
    'position' : 'relative',
    'display' : 'block',
    'height' : '100%',
    'cursor' : 'pointer',
    'borderRadius' : 'inherit',
    'backgroundColor' : 'rgba(0, 0, 0, 0.2)',
    'width' : '0px',
}

def cart_item(idx: int, item: TCartItem = None):
    pid = prefix(f'cart_item_{idx}')

    state = CartContext.getState()

    remove_btn = html.A("×", className='product-remove', id=pid('remove_btn'), href='#')

    @CartContext.On(remove_btn.input.n_clicks)
    def remove_cb(clicks):
        state.items.pop(idx)

    if item:
        return html.Li([
            html.Img(className='product-image', src=item.image),
            html.Div([
                html.P(item.name, className='product-name'),
                html.P(item.price, className='product-price')
            ], className='product-info'),
            html.Div([
                html.P(f"{item.count} Nos.", className='quantity'),
                html.P(f"{item.count * item.price}", className='amount')
            ], className='product-total'),
            remove_btn
        ], className='cart-item')
    else:
        return html.Li(remove_btn, hidden=True)


def cart_info():
    state = CartContext.getState()

    total = 0
    for item in state.items:
        total += item.price * item.count

    return  html.Div([
        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td("No. of items"),
                    html.Td(":"),
                    html.Td([
                        html.Strong(len(state.items))
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

    def empty_cart():
        return  html.Div([
                html.Img(src=EMPTY_CART, alt='empty-cart'),
                html.H2("You cart is empty!")
            ], className='empty-cart')

    state = CartContext.getState()
    if not state.items:
        cart = empty_cart()
        btn_className = 'disabled'
    else:
        cart = html.Ul([cart_item(idx,item) for idx, item in enumerate(state.items)])
        btn_className = ''
    return html.Div([
            html.Div([
                html.Div(cart, style={'position': 'absolute', 'inset': '0px', 'overflow': 'scroll', 'marginRight': '-17px', 'marginBottom': '-17px'}),
                html.Div(html.Div(style=STYLE), style={'position': 'absolute', 'height': '6px', 'right': '2px', 'bottom': '2px', 'left': '2px', 'borderRadius': '3px'}),
                html.Div(html.Div(style=STYLE), style={'position': 'absolute', 'width': '6px', 'right': '2px', 'bottom': '2px', 'top': '2px', 'borderRadius': '3px'})
            ], style={'position': 'relative', 'overflow': 'hidden', 'width': '360px', 'height': '320px'}),
            html.Div(html.Button("PROCEED TO CHECKOUT", type='button', className=btn_className), className='action-block')
        ], className='cart-preview')

def cart():
    state = CartContext.getState()

    # We need to prime the cart with a number of hidden/dummy
    # list items. This is needed because all callbacks must be
    # defined on stat up.

    if not state.items:
        dummy_cart_items = [cart_item(i, None) for i in range(30)]
    else:
        dummy_cart_items = []


    style = {'background': 'none', 'border': 'none'}
    bag_icon = DropdownAIO.Button(html.Img(className='', src=BAG_IMG, alt='Cart'), className='btn btn-link cart-icon', style=style)

    cart_dropdown = DropdownAIO(bag_icon, cart_preview(), id='cart_icon', classname_modifier='active')

    return  html.Div([
        cart_info(),
        cart_dropdown,
        cart_preview(),
        html.Div(dummy_cart_items, hidden=True)
    ], className='cart')
