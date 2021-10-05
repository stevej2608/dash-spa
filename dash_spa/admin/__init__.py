from .views.view_common import blueprint as admin_blueprint

from .views.login_view import login, logout
from .views.register_view import register
from .views.verify_view import verify
from .views.forgot_view import forgot
from .views.users.users_view import user_view
from .views.navbar import AdminNavbarComponent

from .login_manager import AdminLoginManager
