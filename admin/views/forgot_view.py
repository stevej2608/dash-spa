from flask import current_app as app

from flask import session
from enum import Enum

from utils import log, email_valid
from dash import html

from dash_spa import SpaComponents

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


@admin.route('/forgot')
def forgot(ctx):
    """
    Display email form and wait input. If the user enters a valid email
    the login_manager will send an forgot validation email to the user. We
    redirect to the `forgot-code` endpoint
    """
    spa = admin.get_spa()

    flash = spa.Flash(id='flash')
    email = spa.Input(name='email', type='email', id='email', placeholder="Enter email", feedback="Your email is invalid")
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash, email, spa.Button('Reset Request', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

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


@admin.route('/forgot1')
def forgot_code(ctx):
    """
    The user has been sent an email containing the forgot password verification
    code. Allow the user to enter the code. If it verifies we redirect to
    the `forgot2` endpoint.
    """
    spa = admin.get_spa()

    flash = spa.Flash(id='flash')
    code = spa.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash, code, spa.Button('Enter Verification Code', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

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


@admin.route('/forgot2')
def forgot_password(ctx):
    """
    The user has confirmed his email, allow user to change the account
    password
    """
    spa = admin.get_spa()

    flash = spa.Flash(id='flash')
    password = spa.PasswordInput("Password", name='password', id='password', prompt="Make sure your password is strong and easy to remember", placeholder="Enter password")
    confirm_password = spa.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, reenter them")
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash, password, confirm_password, spa.Button('Update Password', id='btn', type='submit')
    ], id='forgot')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data], [SpaComponents.url.state.href])
    def _form_submit(values, href):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

        if ctx.isTriggered(form.input.form_data):
            qs = spa.querystring_args(href)
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
