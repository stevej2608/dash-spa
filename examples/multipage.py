from dash import html
from dash_spa import spa, Blueprint

from app import app as dash_app
from server import serve_app

demo = Blueprint('demo')

NAV_BAR_ITEMS = {
    'brand' : {'title' : 'SPA/Example', 'href' : '/'},
    'left' : [
        {'title' : 'Page1', 'href' : '/demo/page1'},
        {'title' : 'Page2', 'href' : '/demo/page2'},
    ],
}

def big_center(text):
    return html.H2(text, className='display-3 text-center')

@demo.route('/page1')
def test1():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 1'),
    ])

@demo.route('/page2')
def test2():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 2'),
    ])

class CustomSpaApp(spa.SinglePageApp):
    """Example of customising Navbar & Footer

    https://en.wikipedia.org/wiki/Web_colors
    """

    def navBar(self, navitems):
        return super().navBar(navitems, color='DarkSlateGray')

    def footer_text(self):
        return 'Multi-page Example'


def create_app():
    app = CustomSpaApp(dash_app, navitems=NAV_BAR_ITEMS)
    app.register_blueprint(demo, url_prefix='/demo')

    app.layout()

    return app.dash.server

#
# python -m examples.multipage
#

if __name__ == '__main__':
    app = create_app()
    serve_app(app,"/demo/page1")
