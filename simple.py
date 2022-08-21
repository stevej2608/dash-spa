from dash import html
import dash_bootstrap_components as dbc
from dash_spa import DashSPA, page_container, register_page
from server import serve_app

app = DashSPA(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

def big_center(text):
    className='display-3 text-center'
    return html.H2(text, className=className)

def page_layout():
    return big_center('Simple Page Example')

page = register_page("test.page1", path='/page1', title='Page1', layout=page_layout)

if __name__ == "__main__":
    app.layout = page_container
    serve_app(app, debug=False, path=page.path)