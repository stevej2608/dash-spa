from dash import Dash
from dash import html
from app import create_dash
from dash_spa import page_container
from dash_spa import logging, config
from dash_spa.utils import DashLogger, DEBUG_LEVEL
from server import serve_app

from dash_spa_admin import AdminLoginManager

options = config.get('logging')

def create_app(dash_factory) -> Dash:
    """Create Dash application

    Args:
        dash_factory (Dash): Callable that returns a Dash Instance

    Returns:
        Dash: Dash instance
    """
    app = dash_factory()

    def layout():
        return page_container

    app.layout = layout

    if AdminLoginManager.enabled:
        login_manager = AdminLoginManager(app.server)
        login_manager.init_app(app.server)

        # Optionally add admin user here or via the admin web interface
        # if login_manager.user_count() == 0:
        #     login_manager.add_user("admin", "bigjoe@gmail.com", "1234", role=['admin'])


        # Other users can also be added here. Alternatively login as 'admin'
        # and manage users from the users view.

        # if not login_manager.get_user("littlejoe@gmail.com"):
        #     login_manager.add_user("littlejoe", "littlejoe@gmail.com", "5678")

    return app


if __name__ == "__main__":

    logging.setLevel(options.level)

    app = create_app(create_dash)
    logger=DashLogger(DEBUG_LEVEL.VERBOSE)
    serve_app(app, debug=False, logger=logger)

    # serve_app(app, debug=False)
