from dash import html, register_page, callback, no_update as NOUPDATE
from dash_spa import prefix

register_page(__name__, path='/welcome', title='Welcome')

header_text = """
Dash/SPA is a minimal framework and component suite that allows you to build complex
Dash based single-page applications with ease. The demo application includes
several well known Dash examples that have been pasted into the SPA framework
to show how easy it is to transition to SPA.

The framework, component suite and demo are 100% Python
"""

def jumbotron_header(title, text):
    return html.Header([
        html.H1(title, className='display-4 text-center'),
        html.P(text),
    ], className='jumbotron my-4')


def card(title, text):
    return html.Div([
        html.Div([
            html.Img(alt=''),
            html.Div([
                html.H4(title, className='card-title'),
                html.P(text, className='card-text')
            ], className='card-body'),
            html.Div([
            ], className='card-footer')
            ], className='card h-100')
    ], className='col-lg-3 col-md-6 mb-4')


def layout():
    return html.Div([
        jumbotron_header('Welcome to Dash/SPA', header_text),
        html.Div([
            card('Pages', 'Support for Dash Pages, '),
            card('Navbar', 'Includes an optional NAVBAR, configured by a simple dictionary'),
            card('Forms', 'Easy creation of interactive forms'),
            card('Admin', 'Admin blueprint that supports user registration, email authentication and login authorization')
        ], className='row text-center'),
    ], className='container')

