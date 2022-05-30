from usage import create_dash
from dash_spa import page_container
from dash_spa_admin import AdminLoginManager

# Stub for running on pythonAnywhere

dash = create_dash()
dash.layout = page_container

if AdminLoginManager.enabled:
    login_manager = AdminLoginManager(dash.server)
    login_manager.init_app(dash.server)

app = dash.server
