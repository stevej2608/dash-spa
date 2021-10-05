import dash_spa as spa
from dash_spa.admin import AdminNavbarComponent
from app import create_dash

from server import serve_app

NAV_BAR_ITEMS = {
    'brand' : spa.NavbarBrand('Dash/SPA','/'),
    'right': [
        # spa.NavbarLink('Register','/admin/register', icon = "fa fa-user"),
        AdminNavbarComponent()
    ],

}

def create_spa(dash_factory):
    """Create SPA application, return Flask app server instance"""

    app = spa.SinglePageApp(dash_factory, navitems=NAV_BAR_ITEMS)
    app.layout()

    return app.dash.server

if __name__ == '__main__':
    app = create_spa(create_dash)
    serve_app(app, "/admin/login", debug=True)
