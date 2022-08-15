from flask import current_app as app
import dash_holoniq_components as dhc

from dash_spa import callback, NOUPDATE
from dash_spa.logging import log

from .common import LOGOUT_ENDPOINT


def logoutView(ctx):

    redirect = dhc.Location(id='redirect', refresh=True)

    @callback(redirect.output.href, redirect.input.pathname)
    def _logout_cb(pathname):
        log.info('_logout_cb pathname=%s',pathname)
        if pathname == ctx.path_for(LOGOUT_ENDPOINT):
            app.login_manager.logout_user()
            return '/'
        return NOUPDATE

    return redirect
