from flask import session, current_app as app
from flask_login import current_user as flask_current_user


class CurrentUser:
    """Stub that allows Dash/SPA to think it's got a Flask_Login
    login manager when it hasn't. Without a login manager the
    stub mocks the equivalent of an anonymous user. With a login
    manager installed requests are handled by the flask_login
    current_user instance as the would be normally.

    To enable the Dash/SPA login manager add the following lines
    to your start-up code:
    ```
    import dash
    from dash_spa_admin import AdminLoginManager

    app = dash.Dash( __name__, ...)

    ...

    login_manager = AdminLoginManager(app.server)
    login_manager.init_app(app.server)
    ```

    """

    @property
    def is_authenticated(self):
        try:
            session.permanent = True
            return flask_current_user.is_authenticated
        except:
            return
        return False

    @property
    def is_active(self):
        try:
            return flask_current_user.is_active
        except:
            return False

    def get_id(self):
        try:
            return flask_current_user.get_id
        except:
            return

    @property
    def is_anonymous(self):
        try:
            return flask_current_user.is_anonymous
        except:
            return True

    @property
    def role(self):
        try:
            return flask_current_user.role
        except:
            return None

    @property
    def name(self):
        try:
            return flask_current_user.name
        except:
            return "Guest"


current_user = CurrentUser()

def set_current_user(flask_currentuser):
    current_user = flask_currentuser
