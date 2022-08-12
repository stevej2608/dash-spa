from dash import html
from dash_spa import register_page

page1 = register_page(__name__, path='/page1', title='Page1')

def big_center(text, id=None):
    className='display-3 text-center'
    return html.H2(text, id=id, className=className) if id else html.H2(text, className=className)


def layout():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 1', id="page"),
    ])
