from flask import current_app as app

from dash import dcc
from dash import html

from dash_spa import SpaComponents, SpaForm
from .view_common import blueprint as admin
from .view_common import form_layout

@admin.route('/verify', title='Admin verify', prefix_ids=False)
def verify(ctx):

    frm = SpaForm(ctx)

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href='/admin/register')
        ], className="mt-4 text-center")

    flash = frm.Alert(id='flash')
    code = frm.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    button = frm.Button('Submit', type='submit', id='btn')
    redirect = frm.Location(id='redirect', refresh=True)

    form = frm.Form([
        flash,
        code, html.Br(),
        button,
        registerLink()
    ], id='verify')

    @admin.callback([redirect.output.href, flash.output.children], [form.input.form_data], [SpaComponents.url.state.href])
    def _button_click(values, href):
        redirect = frm.NOUPDATE
        error = frm.NOUPDATE

        if ctx.isTriggered(form.input.form_data):
            qs = ctx.querystring_args(href)
            if qs is not None and 'email' in qs:
                code = values['code']
                email = qs['email'][0]
                if app.login_manager.validate(email, code):
                    redirect = admin.url_for('login')
                else:
                    error = 'invalid code, please re-enter'
        return redirect, error

    layout = form_layout('Verify', form)
    return html.Div([layout, redirect])
