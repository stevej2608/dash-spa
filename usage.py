import dash_spa as spa
from admin import admin, login_manager, AdminNavbarComponent
from app import app
from demo import spa as demo
from index import spa as welcome
from server import serve_app
from user import spa as user

NAV_BAR_ITEMS = {
    'brand' : spa.NavbarBrand('Dash/SPA','/'),
    'left' : [
        spa.NavbarLink('Global Warming','/demo/warming'),
        spa.NavbarLink('State Solar', '/demo/solar'),
        spa.NavbarLink('Ticker', '/demo/ticker?tickers=COKE'),
        spa.NavbarLink('Profile', '/user/profile'),
    ],
    'right': [
        AdminNavbarComponent()
    ],

    'footer': spa.Footer('SPA/Examples'),
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
    serve_app(app, "/admin/login", debug=False)
