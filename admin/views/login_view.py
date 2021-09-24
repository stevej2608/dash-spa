from utils import log
from dash import html, dcc

from dash_spa import SpaComponents

from admin.login_manager import login_manager

from admin.views.view_common import form_layout
from admin.views.view_common import blueprint as admin


@admin.route('/login', anonymouse_only=True, title='Admin login')
def login():
    spa = admin.get_spa('login')
    log.info('spa pathname=%s ', spa.get_pathname())

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href=admin.url_for('register'))
        ], className="mt-4 text-center")

    flash = spa.Flash(id='flash')
    email = spa.Input('Email', name='email', type='email', placeholder="Enter email")

    password = spa.PasswordInput("Password", name='password', placeholder="Enter password")
    password.children.insert(1, dcc.Link('Forgot Password?', href=admin.url_for('forgot'), className="float-right"))


    remember = spa.Checkbox("Remember me", id='remember', checked=True)
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


    @spa.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE
        if values:
            email = values['email']
            password = values['password']
            remember = values['admin-login-remember']
            valid = login_manager.login(email, password, remember)
            if valid:
                redirect = admin.url_for('user.profile')
            else:
                error = 'Please check your login details and try again.'

        return redirect, error

    layout = form_layout('Login', form)
    return html.Div([layout, redirect])

@admin.route('/logout', login_required=True)
def logout():
    spa = admin.get_spa('logout')

    redirect = spa.Redirect(id='redirect', refresh=True)

    @spa.callback(redirect.output.href, [SpaComponents.url.input.pathname])
    def _logout_cb(pathname):
        if pathname == admin.url_for('logout'):
            login_manager.logout_user()
            return admin.url_for('user.profile')
        return SpaComponents.NOUPDATE

    return redirect
