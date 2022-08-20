from functools import wraps
from .spa_current_app import current_app

from .exceptions import InvalidAccess
from .spa_current_user import current_user

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        if current_app and current_app.got_first_request:
                if current_user is None or current_user.is_anonymous:
                    raise InvalidAccess(f'You must be logged in to access this page')
        return func(*args, **kwargs)
    return decorated_function