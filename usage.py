from utils import log, logging
import dash_spa as spa

from app import app

from admin import admin
from admin import login_manager

from user import spa as user
from demo import spa as demo
from index import spa as welcome


NAV_BAR_ITEMS = {
    'brand' : {'title' : 'Dash/SPA', 'href' : '/'},
    'left' : [
        {'title' : 'Global Warming', 'endpoint' : 'demo.warming'},
        {'title' : 'State Solar', 'endpoint' : 'demo.solar'},
        {'title' : 'Ticker', 'endpoint' : 'demo.ticker?tickers=COKE'},
        {'title' : 'Profile', 'endpoint' : 'user.profile'},
    ],
    'right': [
        {'title' : 'Login', 'endpoint' : 'admin.login', "login_required" : False, 'icon' : "fa fa-sign-in"},
        {'title' : 'Logout', 'endpoint' : 'admin.logout', "login_required" : True, 'icon' : "fa fa-sign-in"},
        {'title' : 'Register', 'endpoint' : 'admin.register', "login_required" : False, 'icon' : "fa fa-user"},
    ]
}

app = spa.SinglePageApp(app, navitems=NAV_BAR_ITEMS)

app.register_blueprint(welcome, url_prefix='/')
app.register_blueprint(demo, url_prefix='/demo')
app.register_blueprint(user, url_prefix='/user')

app.register_blueprint(admin, url_prefix='/admin')
app.enable_login_manager(login_manager, login_view='admin.login')

if __name__ == '__main__':

    # Turn off werkzeug  logging as it's very noisy

    aps_log = logging.getLogger('werkzeug')
    aps_log.setLevel(logging.ERROR)

    # Set SPA logging level (if needed)

    log.setLevel(logging.INFO)

    print('\nvisit http://localhost:8050/\n')

    app.run_server(debug=False, threaded=False)
