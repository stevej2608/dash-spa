from flask import current_app as app
from dash import html

from dash_spa import isTriggered, location, callback
from dash_spa.logging import log

from .common import form_layout, email_valid, FORGOT_PASSWORD_ENDPOINT

"""
The user has been sent an email containing the forgot password verification
code. Allow the user to enter the code. If it verifies we redirect to
the `forgot2` endpoint.
"""

def forgotCodeForm(ctx):

    frm = ctx.SpaForm(__name__)

    flash = frm.Alert(id='flash')
    code = frm.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, code, frm.Button('Enter Verification Code', id='btn', type='submit')
    ], id='forgot')

    @callback(redirect.output.href, flash.output.children, form.input.form_data, location.state.href)
    def _form_submit(values, href):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if isTriggered(form.input.form_data):
            code = values['code']
            qs = frm.querystring_args(href)
            email = qs['email']
            if not app.login_manager.forgot_code_valid(code, email):
                error = 'Invalid vaildation code, please re-enter'
            else:
                args = {'code': code.upper(), 'email': email}
                redirect = ctx.path_for(FORGOT_PASSWORD_ENDPOINT, args=args)

        return redirect, error

    _form = form_layout('Password Reset', form)

    return html.Div([_form, redirect])
