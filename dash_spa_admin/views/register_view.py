from flask import current_app as app
from dash import html, dcc

from dash_spa import isTriggered, callback, url_for, NOUPDATE
from dash_spa.logging import log

from .common import form_layout, email_valid, form_values, USER, LOGIN_ENDPOINT, REGISTER_VERIFY_ENDPOINT

def registerForm(ctx):

    frm = ctx.SpaForm(__name__)

    def terms_check_box():
        try:
            href=url_for('pages.terms_and_conditions')
            check_box = frm.Checkbox(label=[
                "I agree to the ",
                html.A("Terms and Conditions", href=href)
            ], id='terms', name='terms')
            return [check_box, html.Br()]
        except:
            # User hasn't created a T&C page
            return []

    def accountLink():
        return html.Div([
            "Already have an account? ",
            dcc.Link("Login", href=ctx.path_for(LOGIN_ENDPOINT))
            ], className="mt-4 text-center")

    flash = frm.Alert(id='flash')
    name = frm.Input('Name', name='name', id='name', placeholder="Enter name")
    email = frm.Input('Email', name='email', type='email', id='email', placeholder="Enter email", feedback="Your email is invalid")
    password = frm.PasswordInput("Password", name='password', id='password', prompt="Make sure your password is strong and easy to remember", placeholder="Enter password")
    confirm_password = frm.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, re-enter them")
    terms = terms_check_box()

    redirect = frm.Location(id='redirect', refresh=True)

    button = frm.Button('Register', type='submit', id='btn')

    form = frm.Form([
        flash,
        name,
        email,
        password,
        confirm_password,
        *terms,
        button,
        accountLink()
    ], id='register')

    @callback(redirect.output.href, flash.output.children, form.input.form_data)
    def _form_submit(values):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if isTriggered(form.input.form_data):
            f = form_values(values)

            if not (f.name and f.password and f.confirm_password and f.email):
                error = 'You must enter all fields'
            elif not email_valid(f.email):
                error = 'Invalid email'
            elif f.password != f.confirm_password:
                error = 'Password mismatch'
            elif terms and not f.terms:
                error = 'You must agree to the terms'
            else:
                _terms = False if not terms else f.terms
                code = app.login_manager.register(f.name, f.email, f.password, _terms)
                if code == USER.VALIDATED:
                    redirect = ctx.path_for(LOGIN_ENDPOINT)
                elif code == USER.EMAIL_SENT:
                    redirect = ctx.path_for(REGISTER_VERIFY_ENDPOINT, args={'email': f.email})
                else:
                    error = 'You already have an account, please login as normal'

        return redirect, error

    _form = form_layout('Register', form)
    return html.Div([_form, redirect])

