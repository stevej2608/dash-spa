from flask import current_app as app
from dash import html

from dash_spa import isTriggered, callback, location
from dash_spa.logging import log

from .common import form_layout, LOGIN_ENDPOINT

"""
The user has confirmed his email, allow user to change the account
password
"""

def forgotPasswordForm(ctx):

    frm = ctx.SpaForm(__name__)

    flash = frm.Alert(id='flash')
    password = frm.PasswordInput("Password", name='password', id='password', prompt="Make sure your password is strong and easy to remember", placeholder="Enter password")
    confirm_password = frm.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, re-enter them")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, password, confirm_password, frm.Button('Update Password', id='btn', type='submit')
    ], id='forgot')

    @callback(redirect.output.href, flash.output.children, form.input.form_data, location.state.href)
    def _form_submit(values, href):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if isTriggered(form.input.form_data):
            qs = frm.querystring_args(href)
            if qs is not None and 'code' in qs and 'email' in qs:
                code = qs['code']
                email = qs['email']
                if app.login_manager.forgot_code_valid(code, email):
                    password = values['password']
                    confirm_password = values['confirm_password']
                    if password != confirm_password:
                        error = 'Password mismatch'
                    else:
                        if app.login_manager.change_password(email, password):
                            redirect = ctx.path_for(LOGIN_ENDPOINT)
                        else:
                            error = 'Update failed, try again'

        return redirect, error


    _form = form_layout('Password Reset', form)
    return html.Div([_form, redirect])
