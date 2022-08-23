# dash-spa

**DashSPA** is a component and suite that allows you to build complex
[Plotly/Dash] based multi-page applications with ease. The demo application includes
several well known Dash demos that have been pasted into the SPA framework
to show how easy it is to transition to SPA.

To appreciate what you can do with **DashSPA** take a look at [dash-flightdeck].

![](https://raw.githubusercontent.com/stevej2608/dash-spa/master/docs/img/dash-spa.png)


**Code Snippet**

    pip install dash-spa

```
from dash import html
import dash_bootstrap_components as dbc
from dash_spa import DashSPA, page_container, register_page
from server import serve_app

app = DashSPA(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

def big_center(text):
    className='display-3 text-center'
    return html.H2(text, className=className)

def page_layout():
    return big_center('Simple Page Example')

page = register_page("test.page1", path='/page1', title='Page1', layout=page_layout)

if __name__ == "__main__":
    app.layout = page_container
    serve_app(app, debug=False, path=page.path)
```

**DashSPA** manages component IDs using page namespaces. This greatly
reduces Dash component ID conflicts. A component ID is only ever defined once when the
component is created. It is then used by reference in associated Dash callbacks:

```
from dash import html
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc

from dash_spa import register_page, callback

page = register_page(__name__, ...')

user_name = dbc.Input(id=page.id('user'), placeholder="Enter name")
password = dhc.PasswordInput("Password", name='password', id=page.id('password'), placeholder="Enter password")

btn = html.Button('Enter', id=page.id('enter'), disabled=True)

@callback(btn.output.disabled, user_name.input.value, password.input.value)
def _cb_enter(user_name, password):
    return not db_validate_user(user_name, password)

```

**DashSPA** Defines a state/event pattern where a state Context is wrapped by
a @Context.Provider. Dash callback events update the contexts' state which
triggers the method decorated by the active @Context.Provider. The decorated
method then updates the UI based on the new context state.

A context can have any number of @Context.Providers. This pattern makes it
possible to create generic Dash components that communicate with host
application via ContextState.

ContextState can, if required, have session persistence.

Example usage:
```
@dataclass
class ButtonState(ContextState):
    clicks: int = 0

ButtonContext = createContext(ButtonState)

def Button(id):
    state = ButtonContext.getState()
    btn = html.Button("Button", id=id)

    @ButtonContext.On(btn.input.n_clicks)
    def btn_click(clicks):
        state.clicks += 1


@ButtonContext.Provider()
def layout():
    state = ButtonContext.getState()
    btn =  Button(id='test_btn')
    return html.Div(f"button pressed {state.clicks} times!")
```

**DashSPA** Tables

It's easy it create great looking tables with optional search and pagination. Table cells
can contain text and active components. Table, search and pagination layout is completely flexible.

![](https://raw.githubusercontent.com/stevej2608/dash-spa/master/docs/img/tables-1.png)

Tables are defined in a few lines:

```
def create_table(id):

    state = TableContext.getState()

    df1 = filter_str(df, state.search_term)

    ordersTable = OrdersTable(
        data=df1.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        page = state.current_page,
        page_size = state.page_size,
        id=id
    )

    return ordersTable
```

Tables are customised by creating a custom *tableRow* method for the table:

```
def tableRow(self, index, args):
    name, views, value, rate, change = args.values()
    icon = UP if change == "Up" else DOWN
    return  html.Tr([
        html.Th(name, className='text-gray-900', scope='row'),
        html.Td(views, className='fw-bolder text-gray-500'),
        html.Td(value, className='fw-bolder text-gray-500'),
        html.Td([
            html.Div([
                icon,
                rate
            ], className='d-flex')
        ], className='fw-bolder text-gray-500')
    ])
```

![](https://raw.githubusercontent.com/stevej2608/dash-spa/master/docs/img/tables-2.png)


**DashSPA** Allows easy creation of interactive forms

```
from dash_spa import SpaForm, isTriggered

frm = SpaForm('loginFrm')

email = frm.Input('Email', name='email', type='email', placeholder="Enter email")
password = frm.PasswordInput("Password", name='password', placeholder="Enter password")
button = html.Button('Sign In', type='submit')

form = frm.Form([
    email,
    password,
    button,
], title='Sign In'),


@app.callback(form.output.children, form.input.form_data)
def _form_submit(values):

    if isTriggered(form.input.form_data):
        print(values)

    return spa.NOUPDATE
```

**DashSPA** Supports page containers.

Page containers define markup wrappers for page content. This allows
layout themes to be created. In DashSPA all pages are rendered in
a *default* container but only if one has been defined. If a default
container is not defined the page is rendered raw.

To define a default container, in any module in the ./pages folder:

*/pages/<any_module>.py*
```
from dash import html
import dash_spa as spa

# Example DashSPA container

def my_container(page, layout,  **kwargs):
    try:
        # Page to be rendered

        CONTENT = layout(**kwargs) if callable(layout) else layout

        # Return the container markup with the content embedded

        return html.Div([
            MY_NAVBAR(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(CONTENT, className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
            MY_FOOTER()
        ])
    except Exception:
        page = spa.page_for('pages.not_found_404')
        return page.layout()


spa.register_container(my_container)
```

Any number of containers can be defined. To use an alternative container
simply register the page specifying the container to use:

    register_page(__name__,..., container='admin')

**DashSPA** Has a server-side session data cache. Back ends are available
for [diskcache] and [REDIS].

The shape of session data is defined using [dataclasses].

```
@session_data()
class ButtonState(SessionContext):
    clicks: int = 0

ctx = session_context(ButtonState)
ctx.clicks += 1
```

Any number of session data objects can be defined.

### Login Manager

**DashSPA** Includes an optional **`LogninManager`** that supports user registration, email
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

![](https://raw.githubusercontent.com/stevej2608/dash-spa/master/docs/img/admin-views.png)

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

[Plotly/Dash]: https://dash.plot.ly/introduction
[diskcache]: https://grantjenks.com/docs/diskcache/
[REDIS]: https://redis.io/
[dataclasses]: https://realpython.com/python-data-classes/
[dash-flightdeck]: https://github.com/stevej2608/dash-flightdeck
