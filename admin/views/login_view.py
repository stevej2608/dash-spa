from flask import current_app as app

from dash import dcc
from dash import html

from dash_spa import SpaComponents

from .view_common import blueprint as admin
from .view_common import form_layout

from utils import email_valid

def build_login_form():
    spa = admin.get_spa("login_form")

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href=admin.url_for('register'))
        ], className="mt-4 text-center")

    flash = spa.Flash(id='flash')
    email = spa.Input('Email', id='email', name='email', type='email', placeholder="Enter email")

    password = spa.PasswordInput("Password", name='password', id="password", placeholder="Enter password")
    password.children.insert(1, dcc.Link('Forgot Password?', href=admin.url_for('forgot'), className="float-right"))

    remember = spa.Checkbox("Remember me", id='remember', name='remember', checked=True)
    button = spa.Button('Sign In', type='submit', id='btn')
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash,
        email,
        password,
        remember, html.Br(),
        button,
        registerLink()
    ], id='login')


    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

        ctx = SpaComponents.CallbackContext()

        if ctx.isTriggered(form.input.form_data):
            email = values['email']
            password = values['password']
            remember = values['remember']
            valid = app.login_manager.login(email, password, remember)
            if valid:
                redirect = admin.url_for('user.profile')
            else:
                error = 'Please check your login details and try again.'

        return redirect, error

    layout = form_layout('Sign in', form)
    return html.Div([layout, redirect])


def build_admin_form():
    spa = admin.get_spa("admin_form")

    flash = spa.Flash(id='flash')

    name = spa.Input('Name', name='name', id='name', placeholder="Enter name")
    email = spa.Input('Email', id='email', name='email', type='email', placeholder="Enter email")

    password = spa.PasswordInput("Password", name='password', id="password", placeholder="Enter password")
    confirm_password = spa.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, reenter them")

    button = spa.Button('Create Admin', type='submit', id='btn')
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash,
        name,
        email,
        password,
        confirm_password,
        button,
    ], id='admin_register')


    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

        ctx = SpaComponents.CallbackContext()

        if ctx.isTriggered(form.input.form_data):
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
                app.login_manager.add_user(name, email, password)
                redirect = admin.url_for('user.profile')

        return redirect, error

    layout = form_layout('Create Admin', form)
    return html.Div([layout, redirect])


@admin.route('/login', title='Admin login')
def login(ctx):
    login_manager = ctx.login_manager

    login_form = build_login_form()
    admin_form = build_admin_form()

    if login_manager.user_count() == 0 :
        return admin_form
    else:
        return login_form

@admin.route('/logout', login_required=True)
def logout():
    spa = admin.get_spa()

    redirect = spa.Redirect(id='redirect', refresh=True)

    @admin.callback(redirect.output.href, [SpaComponents.url.input.pathname])
    def _logout_cb(pathname):
        if pathname == admin.url_for('logout'):
            app.login_manager.logout_user()
            return admin.url_for('user.profile')
        return SpaComponents.NOUPDATE

    return redirect
