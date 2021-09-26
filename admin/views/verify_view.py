from flask import current_app as app

from dash import dcc
from dash import html

from dash_spa import SpaComponents
from .view_common import blueprint as admin
from .view_common import form_layout

@admin.route('/verify', title='Admin verify')
def verify():
    spa = admin.get_spa()

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href='/admin/register')
        ], className="mt-4 text-center")

    flash = spa.Flash(id='flash')
    code = spa.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    button = spa.Button('Submit', type='submit', id='btn')
    redirect = spa.Redirect(id='redirect', refresh=True)

    form = spa.Form([
        flash,
        code, html.Br(),
        button,
        registerLink()
    ], id='verify')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data], [SpaComponents.url.state.href])
    def _button_click(values, href):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE

        ctx = SpaComponents.CallbackContext()
        if ctx.isTriggered(form.input.form_data):
            qs = spa.querystring_args(href)
            if qs is not None and 'email' in qs:
                code = values['code']
                email = qs['email'][0]
                if app.login_manager.validate(email, code):
                    redirect = admin.url_for('login')
                else:
                    error = 'invalid code, please reenter'
        return redirect, error

    layout = form_layout('Verify', form)
    return html.Div([layout, redirect])
