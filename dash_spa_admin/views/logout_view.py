from dash_spa.logging import log
from flask import current_app as app
from dash import callback, no_update as NOUPDATE
import dash_holoniq_components as dhc

from dash_spa import url_for

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
