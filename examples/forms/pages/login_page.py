from dash import html

from dash_spa import register_page, SpaForm, isTriggered, callback

from .common import form_container, store

register_page(__name__, path='/login' , title='Login')

frm = SpaForm('loginFrm')

def terms_check_box():
    return frm.Checkbox(label=[
        "I agree to the ",
        html.A("Terms and Conditions", href="#")
    ], id='terms', name='terms')

flash = frm.Alert(id='flash')
email = frm.Input('Email', id='email', name='email', type='email', placeholder="Enter email")
password = frm.PasswordInput("Password", name='password', id="password", placeholder="Enter password")
remember = frm.Checkbox("Remember me", id='remember', name='remember', checked=True)
terms = terms_check_box()
button = frm.Button('Sign In', type='submit', id='btn')
redirect = frm.Location(id='redirect', refresh=True)

form = frm.Form([
    flash,
    email,
    password,
    remember,
    terms, html.Br(),
    button,
], id='login')


@callback(redirect.output.href, store.output.data, flash.output.children, form.input.form_data)
def _form_submit(values):
    redirect = frm.NOUPDATE
    store = frm.NOUPDATE
    error = ""

    if isTriggered(form.input.form_data) and values:
        _password = values['password']
        valid = _password == '1234'
        if valid:
            store = values.copy()
            redirect = '/wellcome'
        else:
            error = 'Please check your login details and try again (hint, try 1234)'


    return redirect, store, error

_form = form_container('Sign in', form)

layout = html.Div([_form, redirect])
