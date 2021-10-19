from flask import current_app as app

from flask import session
from enum import Enum

import dash_holoniq_components as dhc

from holoniq.utils import email_valid
from dash import html

from dash_spa import SpaComponents, SpaForm

from .view_common import blueprint as admin
from .view_common import form_layout

class ResetState(Enum):
    CONFIRM_EMAIL = 1
    CONFIRM_CODE = 2
    RESET_PASSWORD = 3

def get_state():
    if session:
        state = session.get('reset_state', ResetState.CONFIRM_EMAIL)
        return ResetState(state)

    return ResetState.CONFIRM_EMAIL

def set_state(state):
    if session:
        session['reset_state'] = state.value


@admin.route('/forgot', prefix_ids=False)
def forgot(ctx):
    """
    Display email form and wait input. If the user enters a valid email
    the login_manager will send an forgot validation email to the user. We
    redirect to the `forgot-code` endpoint
    """

    frm = SpaForm(ctx)

    flash = frm.Alert(id='flash')
    email = frm.Input(name='email', type='email', id='email', placeholder="Enter email", feedback="Your email is invalid")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, email, frm.Button('Reset Request', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if ctx.isTriggered(form.input.form_data):
            email = values['email']
            if not email_valid(email):
                error = 'Invalid email'
            elif not app.login_manager.forgot(email):
                error = 'You do not have an account on this site'
            else:

                # An email has been sent to the user, redirect to await
                # entry of the forgot password validation code

                redirect = admin.url_for('forgot1', {'email': email})

        return redirect, error

    layout = form_layout('Password Reset', form)
    return html.Div([layout, redirect])


@admin.route('/forgot1', prefix_ids=False)
def forgot_code(ctx):
    """
    The user has been sent an email containing the forgot password verification
    code. Allow the user to enter the code. If it verifies we redirect to
    the `forgot2` endpoint.
    """
    frm = SpaForm(ctx)

    flash = frm.Alert(id='flash')
    code = frm.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, code, frm.Button('Enter Verification Code', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if ctx.isTriggered(form.input.form_data):
            code = values['code']
            if not app.login_manager.forgot_code_valid(code):
                error = 'Invalid vaildation code, please reenter'
            else:
                args = {'code': code.upper(), 'email': app.login_manager.get_email()}
                redirect = admin.url_for('forgot2', args=args)

        return redirect, error

    layout = form_layout('Password Reset', form)
    return html.Div([layout, redirect])


@admin.route('/forgot2', prefix_ids=False)
def forgot_password(ctx):
    """
    The user has confirmed his email, allow user to change the account
    password
    """
    frm = SpaForm(ctx)

    flash = frm.Alert(id='flash')
    password = frm.PasswordInput("Password", name='password', id='password', prompt="Make sure your password is strong and easy to remember", placeholder="Enter password")
    confirm_password = frm.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, reenter them")
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash, password, confirm_password, frm.Button('Update Password', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data], [SpaComponents.url.state.href])
    def _form_submit(values, href):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if ctx.isTriggered(form.input.form_data):
            qs = ctx.querystring_args(href)
            if qs is not None and 'code' in qs and 'email' in qs:
                code = qs['code'][0]
                email = qs['email'][0]
                if app.login_manager.forgot_code_valid(code):
                    password = values['password']
                    confirm_password = values['confirm_password']
                    if password != confirm_password:
                        error = 'Password mismatch'
                    else:
                        if app.login_manager.change_password(email, password):
                            redirect = admin.url_for('login')
                        else:
                            error = 'Update failed, try again'

        return redirect, error

    layout = form_layout('Password Reset', form)
    return html.Div([layout, redirect])
