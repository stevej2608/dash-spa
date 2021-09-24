from admin.views.view_common import blueprint as admin

from admin.views.login_view import login, logout
from admin.views.register_view import register
from admin.views.verify_view import verify
from admin.views.forgot_view import forgot

from admin.login_manager import login_manager
