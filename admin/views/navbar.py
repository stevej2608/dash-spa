from dash import html
import dash_bootstrap_components as dbc

class AdminNavbarComponent:

    def __init__(self):
        pass

    def account_dropdown(self, app):

        menu = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Messages", href="#"),
                dbc.DropdownMenuItem("Settings", href="#"),
                dbc.DropdownMenuItem([html.I(className='fa fa-sign-in'), ' Sign out'], href='/admin/logout')
             ],
            nav=True,
            in_navbar=True,
            label="My Account",
            right=True
        )

        icon = html.I(className="fa fa fa-user", style={'position': 'relative','left': '4px'})

        return html.Div(['', icon, menu], style={'padding': '0'}, className='d-flex align-items-center nav-link')

    def signin_link(self, spa):
        return dbc.NavItem(
            dbc.NavLink([html.I(className='fa fa-sign-in'), ' Sign in'], href='/admin/login')
        )

    def layout(self, spa):
        if spa.user_logged_in():
            return self.account_dropdown(spa)
        else:
            return self.signin_link(spa)
