from dash import html, dcc

from admin.login_manager import login_manager

from .view_common import blueprint as admin
from .view_common import form_layout

@admin.route('/verify', title='Admin verify')
def verify():
    spa = admin.get_spa('verify')

    def registerLink():
        return html.Div([
            "Don't have an account? ",
            dcc.Link("Create one", href='/admin/register')
        ], className="mt-4 text-center")

    flash = spa.Flash(id='flash')
    code = spa.Input(name='code', id='code', placeholder="verification code", prompt="Check your email in-box")
    button = spa.Button('Submit', type='submit', id='btn')
    redirect = spa.Redirect(id='redirect')

    form = spa.Form([
        flash,
        code, html.Br(),
        button,
        registerLink()
    ], id='verify')

    @spa.callback([redirect.output.href, flash.output.children], [form.input.form_data])
    def _button_click(values):
        redirect = spa.NOUPDATE
        error = spa.NOUPDATE
        if values:
            code = values['code']
            if login_manager.validate(code):
                redirect = admin.url_for('login')
            else:
                error = 'invalid code, please reenter'

        return redirect, error

    layout = form_layout('Verify', form)
    return html.Div([layout, redirect])
