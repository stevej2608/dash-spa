from flask import current_app as app

from dash import dcc
from dash import html

from dash_spa import SpaComponents

from .view_common import blueprint as admin
from .view_common import form_layout, form_values

from utils import email_valid

@admin.route('/register', title='Admin register')
def register():
    spa = admin.get_spa()

    def terms_check_box():
        return spa.Checkbox([
            "I agree to the ",
            html.A("Terms and Conditions", href="#")
        ], id='terms', name='terms')


    def accountLink():
        return html.Div([
            "Already have an account? ",
            dcc.Link("Login", href=admin.url_for('login'))
            ], className="mt-4 text-center")

    flash = spa.Flash(id='flash')
    name = spa.Input('Name', name='name', id='name', placeholder="Enter name")
    email = spa.Input('Email', name='email', type='email', id='email', placeholder="Enter email", feedback="Your email is invalid")
    password = spa.PasswordInput("Password", name='password', id='password', prompt="Make sure your password is strong and easy to remember", placeholder="Enter password")
    confirm_password = spa.PasswordInput('Re-enter password', name="confirm_password", id='confirm_password', placeholder="Re-enter password", feedback="Password fields are not the same, reenter them")
    terms = terms_check_box()

    redirect = spa.Redirect(id='redirect', refresh=True)

    button = spa.Button('Register', type='submit', id='btn')

    form = spa.Form([
        flash,
        name,
        email,
        password,
        confirm_password,
        terms, html.Br(),
        button,
        accountLink()
    ], id='register')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _form_submit(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

        ctx = SpaComponents.CallbackContext()

        if ctx.isTriggered(form.input.form_data):
            f = form_values(values)

            if not (f.name and f.password and f.confirm_password and f.email):
                error = 'You must enter all fields'
            elif not email_valid(f.email):
                error = 'Invalid email'
            elif f.password != f.confirm_password:
                error = 'Password mismatch'
            elif not terms:
                error = 'You must agree to the terms'
            else:
                if app.login_manager.register(f.name, f.email, f.password, f.terms):
                    redirect = admin.url_for('verify', args={'email': f.email})
                else:
                    error = 'You already have an account, please login as normal'

        return redirect, error

    layout = form_layout('Register', form)
    return html.Div([layout, redirect])
