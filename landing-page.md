# dash-spa

**Dash/SPA** is a minimal template and component suite that allows you to build complex 
**[Dash](https://dash.plot.ly/introduction)** based multi-page applications with ease. The demo application includes
several well known Dash demos that have been pasted into the SPA framework
to show how easy it is to transition to SPA.

**Dash/SPA** supports Flask style Blueprints and route decorators:

![](https://raw.githubusercontent.com/stevej2608/dash-spa/main/docs/img/signin.png)

**Code Snippet**

    pip install dash-spa

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
    'brand' : spa.NavbarBrand('Dash/SPA','/'),
    'left' : [
        spa.NavbarLink('Global Warming','/demo/warming'),
        spa.NavbarLink('State Solar', '/demo/solar'),
        spa.NavbarLink('Ticker', '/demo/ticker?tickers=COKE'),
        spa.NavbarLink('Profile', '/user/profile'),
        spa.NavbarLink('Admin', '/admin/users'),
    ],
    'right': [
        AdminNavbarComponent()
    ],

    'footer': spa.Footer('SPA/Examples'),
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

## Admin Blueprint

**Dash/SPA** Includes an optional **`admin`** blueprint that supports user registration, email 
authentication and login. This is provided as a demonstrator, careful consideration
to the security implications should be undertaken before using it in a public website.

Views are provided that allow:

* Register, name, email, password. Verification code send by email.
* Enter the email verification code.

* Normal user login.
 
* Reset forgotten password, Password reset code sent by email.
* Enter password reset code.
* Enter new password, confirm new password.
* Login using new password.

* User admin table with Add, Edit and Delete. Accessible only when signed in with *admin* rights.


![](https://raw.githubusercontent.com/stevej2608/dash-spa/main/docs/img/admin-views.png)

## Documentation

Head over to the [*README*][docs-homepage] for more details.

## Contributing

The source code for *dash-spa* is available
[on GitHub][dash-spa-repo]. If you find a bug or something is unclear, we encourage
you to raise an issue. We also welcome contributions, to contribute, fork the
repository and open a [pull request][dash-spa-pulls].


[dash-homepage]: https://dash.plot.ly/
[dash-spa-repo]: https://github.com/stevej2608/dash-spa
[docs-homepage]: https://github.com/stevej2608/dash-spa/blob/master/README.md
[dash-spa-pulls]: https://github.com/stevej2608/dash-spa/pulls
