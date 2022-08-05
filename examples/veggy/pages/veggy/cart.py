from dash import html
from dash_spa.components.dropdown_aio import DropdownAIO
from dash_spa.spa_context import  createContext, ContextState, dataclass

BAG_IMG = 'https://res.cloudinary.com/sivadass/image/upload/v1493548928/icons/bag.png'
EMPTY_CART = 'https://res.cloudinary.com/sivadass/image/upload/v1495427934/icons/empty-cart.png'


@dataclass
class TCartItem(ContextState):
    id: str = None
    count: int = 0


@dataclass
class TCartState(ContextState):
    isCartOpen: bool = False
    items: list = None

CartContext = createContext(TCartState)


STYLE = {
    'position' : 'relative',
    'display' : 'block',
    'height' : '100%',
    'cursor' : 'pointer',
    'border-radius' : 'inherit',
    'background-color' : 'rgba(0, 0, 0, 0.2)',
    'width' : '0px',
}

def cart_info():
    state = CartContext.getState()
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
    state = CartContext.getState()
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src=EMPTY_CART, alt='empty-cart'),
                        html.H2("You cart is empty!")
                    ], className='empty-cart')
                ], style={'position': 'absolute', 'inset': '0px', 'overflow': 'scroll', 'margin-right': '-17px', 'margin-bottom': '-17px'}),
                html.Div(html.Div(style=STYLE), style={'position': 'absolute', 'height': '6px', 'right': '2px', 'bottom': '2px', 'left': '2px', 'border-radius': '3px'}),
                html.Div(html.Div(style=STYLE), style={'position': 'absolute', 'width': '6px', 'right': '2px', 'bottom': '2px', 'top': '2px', 'border-radius': '3px'})
            ], style={'position': 'relative', 'overflow': 'hidden', 'width': '360px', 'height': '320px'}),
            html.Div(html.Button("PROCEED TO CHECKOUT", type='button', className='disabled'), className='action-block')
        ], className='cart-preview')

def cart():

    style = {'background': 'none', 'border': 'none'}
    bag_icon = DropdownAIO.Button(html.Img(className='', src=BAG_IMG, alt='Cart'), className='btn btn-link cart-icon', style=style)

    cart_dropdown = DropdownAIO(bag_icon, cart_preview(), id='cart_icon', classname_modifier='active')

    return  html.Div([
        cart_info(),
        cart_dropdown,
        cart_preview()
    ], className='cart')
