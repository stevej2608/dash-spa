from dash import html
from dash_spa import register_page, callback

from .common import store

register_page(__name__, path='/wellcome', title='Welcome')

def big_center(text):
    if id:
        return html.H2(text, className='display-3 text-center')
    else:
        return html.H2(text, className='display-3 text-center')

def page_content(name='Guest'):

    return html.Header([
        big_center("Dash/SPA Welcomes"),
        big_center(name)
    ], className='jumbotron my-4')


layout = html.Div(page_content(), id='container')

@callback(layout.output.children, store.input.data)
def _page_cb(data):

    if data:
        return page_content(data['email'])
    else:
        return page_content()
