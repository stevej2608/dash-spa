from flask import current_app as app
from dash import html

from dash_spa import isTriggered, location, callback
from dash_spa.logging import log

from .common import form_layout, email_valid, REGISTER_ADMIN_ENDPOINT, LOGIN_ENDPOINT

def adminRegistrationForm(ctx):

    frm = ctx.SpaForm(__name__)

    log.info('__name__=%s', __name__)

    def get_name(value=None):
        return frm.Input('Name', name='name', id='name', placeholder="Enter name", value=value)

    def get_email(value=None):
        return frm.Input('Email', id='email', name='email', type='email', placeholder="Enter email", value=value)

    flash = frm.Alert(id='flash')
    name = get_name()
    email = get_email()
    password = frm.PasswordInput("Password", name='password', id="password", placeholder="Enter password")
    confirm_password = frm.PasswordInput('Re-enter password',
            name="confirm_password", id='confirm_password', placeholder="Re-enter password",
            feedback="Password fields are not the same, re-enter them")
    button = frm.Button('Create Admin', type='submit', id='btn')
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash,
        name,
        email,
        password,
        confirm_password,
        button,
    ], id='admin_register')


    @callback(redirect.output.href, flash.output.children, form.input.form_data)
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = ""

        log.info('_form_submit values=%s', values)

        if isTriggered(form.input.form_data):
            name = values['name']
            email = values['email']
            password = values['password']
            confirm_password = values['confirm_password']
            if not (name and password and confirm_password and email):
                error = 'You must enter all fields'
            elif not email_valid(email):
                error = 'Invalid email'
            elif password != confirm_password:
                error = 'Password mismatch'
            else:
                app.login_manager.add_user(name, email, password, role=['admin'])
                redirect = ctx.path_for(LOGIN_ENDPOINT)


        return redirect, error

    # Make name & email fields persistent.

    store = frm.Store(form, fields=['name', 'email'], storage_type='local')

    @callback(form.output.children, location.input.pathname, store.state.data)
    def _form_update(pathname, data):
        if pathname == ctx.path_for(REGISTER_ADMIN_ENDPOINT) and data is not None:
            name = get_name(data['name'])
            email = get_email(data['email'])
            return [flash, name, email, password, confirm_password, button]
        else:
            return frm.NOUPDATE


    _form = form_layout('Create Admin', form)
    return html.Div([_form, redirect, store])
