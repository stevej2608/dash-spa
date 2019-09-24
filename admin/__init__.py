from .views.view_common import blueprint as admin

from .views.login_view import login, logout
from .views.register_view import register
from .views.verify_view import verify
from .views.forgot_view import forgot

from .login_manager import login_manager
