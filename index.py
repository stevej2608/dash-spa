from dash import html, dcc
from dash_spa import Blueprint

spa = Blueprint('welcome')

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


def card(title, text, link=None):
    return html.Div([
        html.Div([
            html.Img(alt=''),
            html.Div([
                html.H4(title, className='card-title'),
                html.P(text, className='card-text')
            ], className='card-body'),
            html.Div([
                # spa.ButtonLink('Find Out More!', href=spa.url_for(link)).layout
            ], className='card-footer')
            ], className='card h-100')
    ], className='col-lg-3 col-md-6 mb-4')


@spa.route('/')
def index():
    return html.Div([
        jumbotron_header('Welcome to Dash/SPA', header_text),
        html.Div([
            card('Blueprints', 'Supports Flask style Blueprints and route decorators', 'blueprints'),
            card('Navbar', 'Includes an optional NAVBAR, configured by a simple dictionary'),
            card('Forms', 'Easy creation of interactive forms'),
            card('Admin', 'Admin blueprint that supports user registration, email authentication and login authorization')
        ], className='row text-center'),
    ], className='container')


@spa.route('/blueprints')
def blueprints():
    return dcc.Markdown("""
**Dash/SPA** supports Flask style Blueprints and route decorators:

```
    from dash import html
    from dash_spa import Blueprint

    greetings = Blueprint('greetings')

    @greetings.route('/hello')
    def hello():
        return html.H2('Dash/SPA say's HELLO!')

    @greetings.route('/goodby')
    def goodby():
        return html.H2('Dash/SPA say's GOODBY!')

...

app.register_blueprint(greetings, url_prefix='/test/greetings')
```
""")
