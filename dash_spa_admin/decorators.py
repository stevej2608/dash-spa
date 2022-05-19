from functools import wraps
from flask import current_app as app
from flask_login import current_user
from dash_spa.exceptions import InvalidAccess

# TODO: Move this to dash_spa and test role via Flask current user

def role_required(role_name):
    """Layout function decorator. Raise InvalidAccess exception if current user
    does not have the role required

    Args:
        role_name (str): "admin" or "user"

    Raises:

        InvalidAccess exception

    ```
        @role_required('admin')
        def layout():
            return "Secrets known only to admin..."

    ```
    """
    def decorator(func):
        @wraps(func)
        def authorize(*args, **kwargs):
            if app and app.got_first_request:
                if not app.login_manager.isAdmin():
                    raise InvalidAccess(f'You must have "{role_name}" role to access this route')
            return func(*args, **kwargs)
        return authorize
    return decorator
