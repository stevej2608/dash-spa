from dash import html
import dash_spa as spa

from app import create_dash
from server import serve_app

demo = spa.Blueprint('demo')

NAV_BAR_ITEMS = {
    'brand' : spa.NavbarBrand('SPA/Example','/'),
    'left' : [
        spa.NavbarLink('Page1','/demo/page1'),
        spa.NavbarLink('Page2','/demo/page2'),
    ],
    'footer': spa.Footer(),
}

def big_center(text, id=None):
    className='display-3 text-center'
    return html.H2(text, id=id, className=className) if id else html.H2(text, className=className)

@demo.route('/page1')
def test1():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 1', id="page"),
    ])

@demo.route('/page2')
def test2():
    return html.Div([
        big_center('Multi-page Example'),
        big_center('+'),
        big_center('Page 2', id="page"),
    ])

class CustomSpaApp(spa.SinglePageApp):
    """Example of customising Navbar & Footer"""

    # https://en.wikipedia.org/wiki/Web_colors

    def navBar(self, navitems, dark=True, color='secondary'):
        return super().navBar(navitems, dark=dark, color='DarkSlateGray')

    def footer_text(self):
        return 'Multi-page Example'

def create_spa(dash_app):
    app = CustomSpaApp(dash_app, navitems=NAV_BAR_ITEMS)
    app.register_blueprint(demo, url_prefix='/demo')

    app.layout()

    return app

#
# python -m examples.multipage
#

if __name__ == '__main__':
    dash_app = create_dash()
    app = create_spa(dash_app)
    serve_app(app.dash,"/demo/page1")
