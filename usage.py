from utils import log, logging
import dash_spa as spa

from app import app
from server import serve_app

from admin import admin
from admin import login_manager

from user import spa as user
from demo import spa as demo
from index import spa as welcome


NAV_BAR_ITEMS = {
    'brand' : {'title' : 'Dash/SPA', 'href' : '/'},
    'footer': 'SPA/Examples',
    'left' : [
        {'title' : 'Global Warming', 'href' : '/demo/warming'},
        {'title' : 'State Solar', 'href' : '/demo/solar'},
        {'title' : 'Ticker', 'href' : '/demo/ticker?tickers=COKE'},
        {'title' : 'Profile', 'href' : '/user/profile'},
    ],
    'right': [
        {'title' : 'Login', 'href' : '/admin/login', "login_required" : False, 'icon' : "fa fa-sign-in"},
        {'title' : 'Logout', 'href' : '/admin/logout', "login_required" : True, 'icon' : "fa fa-sign-in"},
        {'title' : 'Register', 'href' : '/admin/register', "login_required" : False, 'icon' : "fa fa-user"},
    ]
}

def create_spa(app=app):
    """Create SPA application, return Flask app server instance"""

    app = spa.SinglePageApp(app, navitems=NAV_BAR_ITEMS)

    app.register_blueprint(welcome)
    app.register_blueprint(demo, url_prefix='/demo')
    app.register_blueprint(user, url_prefix='/user')

    app.register_blueprint(admin, url_prefix='/admin')
    app.enable_login_manager(login_manager, login_view='admin.login')

    app.layout()

    return app.dash.server

if __name__ == '__main__':
    app = create_spa()
    serve_app(app, "/admin/login")
