import os
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

app = spa.SinglePageApp(app, navitems=NAV_BAR_ITEMS)

app.register_blueprint(welcome)
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

    port = int(os.environ.get("PORT", 5000))
    hostname = os.environ.get("HOST_HOSTNAME", "localhost")
    hostport = os.environ.get("HOST_HOSTPORT", "5000")

    print(f' * Visit http://{hostname}:{hostport}/admin/login\n')

    app.run_server(debug=False, host='0.0.0.0', port=port, threaded=False)  
