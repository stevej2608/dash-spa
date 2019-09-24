### Dash Single Page Application (SPA) Framework

    pip install -r requirements.txt
    python usage.py

**Dash/SPA** is a minimal template and component suite that allows you to build complex 
**[Dash](https://dash.plot.ly/introduction)** based multi-page applications with ease. The demo application includes
several well known Dash demos that have been pasted into the SPA framework
to show how easy it is to transition to SPA.

**Dash/SPA** supports Flask style Blueprints and route decorators:

```
import dash_html_components as html
from dash_spa import Blueprint

greetings = Blueprint('greetings')

@greetings.route('/hello')
def hello():
    return html.H2('Dash/SPA says HELLO!')

@greetings.route('/goodby')
def goodby():
    return html.H2('Dash/SPA says GOODBY!')

...

app.register_blueprint(greetings, url_prefix='/test/greetings')
```

**Dash/SPA** manages component IDs using blueprint/route based namespaces. This greatly 
reduces Dash component ID conflicts. A component ID is only defined once when the component
is created. It is then used by reference in associated Dash callbacks:

```
    user_name = spa.Input(id='user', placeholder="Enter name")
    password = spa.PasswordInput("Password", name='password', id='password', placeholder="Enter password")

    btn = spa.Button('Enter', id='enter', disabled=True)

    @app.callback(btn.output.disabled, [user_name.input.value, password.input.value])
    def _cb_enter(user_name, password):
        return not db_validate_user(user_name, password)

```

**Dash/SPA** includes an optional NAVBAR, configured by a simple dictionary:

```
NAV_BAR_ITEMS = {
    'brand' : {'title' : 'Dash/SPA', 'href' : '/'},
    'left' : [
        {'title' : 'Global Warming', 'endpoint' : 'demo.warming'},
        {'title' : 'State Solar', 'endpoint' : 'demo.solar'},
        {'title' : 'Ticker', 'endpoint' : 'demo.ticker?tickers=COKE+TSLA'},
    ],
    'right': [
        {'title' : 'Sign In', 'endpoint' : 'admin.login', 'icon' : "fa fa-sign-in"},
        {'title' : 'Register', 'endpoint' : 'admin.register', 'icon' : "fa fa-user"},
    ]
}
```

**Dash/SPA** Allows easy creation of interactive forms

```
        email = spa.Input('Email', name='email', type='email', placeholder="Enter email")
        password = spa.PasswordInput("Password", name='password', placeholder="Enter password")
        button = button = spa.Button('Sign In', type='submit')

        form = spa.Form([
            email,
            password,
            button,
        ], title='Sign In'),


        @spa.callback(form.output.children, [form.input.form_data])
        def _form_submit(values):
            print(values)
            return spa.NOUPDATE


```

## Documentation

For additional documentation and examples visit [dash-spa](https://github.com/stevej2608/dash-spa) 