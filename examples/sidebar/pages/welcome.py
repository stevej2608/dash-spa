from dash import html
from dash_spa import register_page, callback


register_page(__name__, path='/', title='Welcome')

def big_center(text):
    return html.H2(text, className='display-3 text-center')


def page_content(name='Guest'):

    return html.Header([
        big_center("Dash/SPA Welcomes"),
        big_center(name)
    ], className='jumbotron my-4')


layout = html.Div(page_content())

