from flask import current_app as app
from dash import html, dcc
from dash.exceptions import PreventUpdate

from dash_spa import isTriggered, callback, location, url_for
from dash_spa.logging import log

from .common import form_layout, LOGIN_ENDPOINT, FORGOT_ENDPOINT, REGISTER_ENDPOINT

def loginForm(ctx):

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href=ctx.path_for(REGISTER_ENDPOINT))
        ], className="mt-4 text-center")

    frm = ctx.SpaForm(__name__)

    flash = frm.Alert(id='flash')
    email = frm.Input('Email', id='email', name='email', type='email', placeholder="Enter email")

    password = frm.PasswordInput("Password", name='password', id="password", placeholder="Enter password")
    password.children.insert(1, dcc.Link('Forgot Password?', href=ctx.path_for(FORGOT_ENDPOINT), className="float-end"))

    remember = frm.Checkbox("Remember me", id='remember', name='remember', checked=True)
    button = frm.Button('Sign In', type='submit', id='btn')
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash,
        email,
        password,
        remember, html.Br(),
        button,
        registerLink()
    ], id='login')


    @callback(redirect.output.href, flash.output.children, form.input.form_data)
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = ""

        log.info('_form_submit values=%s', values)

        if isTriggered(form.input.form_data):
            email = values['email']
            password = values['password']
            remember = values['remember']
            valid = app.login_manager.login(email, password, remember)
            if valid:
                # TODO: Make this configurable
                redirect = url_for('pages.user.profile')
            else:
                error = 'Please check your login details and try again.'


        return redirect, error

    # Make email field perestant.

    store = frm.Store(form, fields=[email.name, remember.name], storage_type='session')

    @callback(email.output.value, remember.output.value, location.input.pathname, store.state.data)
    def _form_update(pathname, data):
        if pathname == ctx.path_for(LOGIN_ENDPOINT) and data is not None:
            return data[email.name], data[remember.name]

        raise PreventUpdate

    _form = form_layout('Sign in', form)

    return html.Div([_form, redirect, store])
