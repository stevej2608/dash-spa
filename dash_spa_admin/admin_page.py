from dash_spa import callback , NOUPDATE, prefix, SpaForm, register_page
from dash_spa.logging import log

from .views import loginForm, forgotForm, forgotCodeForm, forgotPasswordForm
from .views import registerForm, logoutView, usersView, adminRegistrationForm
from .views import registerVerifyForm

from .views.common import (LOGIN_ENDPOINT, LOGOUT_ENDPOINT,
                           REGISTER_ENDPOINT, REGISTER_ADMIN_ENDPOINT,
                           REGISTER_VERIFY_ENDPOINT,
                           FORGOT_ENDPOINT, FORGOT_CODE_ENDPOINT, FORGOT_PASSWORD_ENDPOINT,
                           USERS_ENDPOINT)

from .exceptions import InvalidPath


class AdminPage:

    def __init__(self, login_manager):
        pfx = prefix('spa_admin')

        database_uri = login_manager.database_uri()

        class ViewContext:

            def path_for(self, endpoint, args=None):
                return login_manager.path_for(endpoint, args)

            def SpaForm(self, id):
                id = id.split('.')[-1]
                return SpaForm(pfx(id))

        ctx = ViewContext()

        views = {
            LOGIN_ENDPOINT: loginForm(ctx),
            LOGOUT_ENDPOINT: logoutView(ctx),

            FORGOT_ENDPOINT:  forgotForm(ctx),
            FORGOT_CODE_ENDPOINT : forgotCodeForm(ctx),
            FORGOT_PASSWORD_ENDPOINT : forgotPasswordForm(ctx),

            REGISTER_ENDPOINT: registerForm(ctx),
            REGISTER_ADMIN_ENDPOINT: adminRegistrationForm(ctx),
            REGISTER_VERIFY_ENDPOINT: registerVerifyForm(ctx),

            USERS_ENDPOINT: usersView(ctx, database_uri)

        }

        # container = html.Div(loginForm, id=pfx('container'))

        # @callback(container.output.children, spa.location.input.pathname)
        # def admin_cb(pathname):
        #     if pathname in views:
        #         return views[pathname]
        #     return NOUPDATE

        # def layout(view_id=LOGIN_ENDPOINT, **kwargs):
        #     log.info('layout "%s"', view_id)
        #     if view_id in views:
        #         return views[view_id]
        #     raise InvalidPath

        # register_page('dash_spa_admin.page', path_template=f'{login_manager.slug}/<view_id>', layout=layout)

        for id, layout in views.items():
            register_page(
                f'dash_spa_admin.{id}',
                path=f'{login_manager.slug}/{id}',
                layout=layout
            )

