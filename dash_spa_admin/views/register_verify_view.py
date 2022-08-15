from flask import current_app as app
from dash import html, dcc

from dash_spa import isTriggered, callback, location
from dash_spa.logging import log

from .common import form_layout, REGISTER_ENDPOINT, LOGIN_ENDPOINT

"""
The user has been sent an email containing the registration verification
code. Allow the user to enter the code. If it verifies we redirect to
the LOGIN_ENDPOINT endpoint.
"""

def registerVerifyForm(ctx):

    frm = ctx.SpaForm(__name__)

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href=ctx.path_for(REGISTER_ENDPOINT))
        ], className="mt-4 text-center")

    flash = frm.Alert(id='flash')
    code = frm.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    button = frm.Button('Submit', type='submit', id='btn')
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash,
        code, html.Br(),
        button,
        registerLink()
    ], id='verify')

    @callback(redirect.output.href, flash.output.children, form.input.form_data, location.state.href)
    def _button_click(values, href):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if isTriggered(form.input.form_data):
            qs = frm.querystring_args(href)
            if qs is not None and 'email' in qs:
                code = values['code']
                email = qs['email']
                if app.login_manager.validate(email, code):
                    redirect = ctx.path_for(LOGIN_ENDPOINT)
                else:
                    error = 'invalid code, please re-enter'
        return redirect, error

    _form = form_layout('Verify', form)
    return html.Div([_form, redirect])