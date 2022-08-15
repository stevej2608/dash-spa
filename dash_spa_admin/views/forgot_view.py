from flask import current_app as app
from dash import html

from dash_spa import isTriggered, callback
from dash_spa.logging import log

from .common import form_layout, email_valid, FORGOT_CODE_ENDPOINT

"""
Display email form and wait input. If the user enters a valid email
the login_manager will send an forgot validation email to the user. We
redirect to the `forgot-code` endpoint
"""

def forgotForm(ctx):

    frm = ctx.SpaForm(__name__)

    flash = frm.Alert(id='flash')
    email = frm.Input(name='email', type='email', id='email', placeholder="Enter email", feedback="Your email is invalid")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, email, frm.Button('Reset Request', id='btn', type='submit')
    ], id='forgot')

    @callback(redirect.output.href, flash.output.children, form.input.form_data)
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if isTriggered(form.input.form_data):
            email = values['email']
            if not email_valid(email):
                error = 'Invalid email'
            elif not app.login_manager.forgot(email):
                error = 'You do not have an account on this site'
            else:

                # An email has been sent to the user, redirect to await
                # entry of the forgot password validation code

                redirect = ctx.path_for(FORGOT_CODE_ENDPOINT, {'email': email})

        return redirect, error

    _form = form_layout('Password Reset', form)
    return html.Div([_form, redirect])
