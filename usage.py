import dash_spa as spa
from admin import admin, AdminLoginManager, AdminNavbarComponent
from app import create_dash
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
        spa.NavbarLink('Admin', '/admin/users'),
    ],
    'right': [
        AdminNavbarComponent()
    ],

    'footer': spa.Footer('SPA/Examples'),
}

def create_spa(dash_app):
    """Create SPA application, return SinglePageApp instance

    Args:
        app (Dash): Dash Instance

    Returns:
        SinglePageApp: Single Page App instance
    """

    app = spa.SinglePageApp(dash_app, navitems=NAV_BAR_ITEMS)

    app.register_blueprint(welcome)
    app.register_blueprint(demo, url_prefix='/demo')
    app.register_blueprint(user, url_prefix='/user')

    # Enable admin

    app.register_blueprint(admin, url_prefix='/admin')
    login_manager = AdminLoginManager(app.dash.server)
    app.enable_login_manager(login_manager, login_view='admin.login')

    app.layout()

    return app

if __name__ == '__main__':
    dash = create_dash()
    app = create_spa(dash)
    serve_app(app.dash, "/admin/users", debug=False)
