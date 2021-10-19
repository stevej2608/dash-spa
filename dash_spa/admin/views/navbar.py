from abc import abstractmethod
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user

class AdminNavbarComponent:

    def __init__(self):
        pass

    @abstractmethod
    def menu_items(self, spa):
        """User defined components for NavBar My Account dropdown"""
        return [
            dbc.DropdownMenuItem("Messages", href="#"),
            dbc.DropdownMenuItem("Settings", href="#"),
        ]

    def account_dropdown(self, spa):

        children = self.menu_items(spa)

        if spa.login_manager.isAdmin():
            users_link = dbc.DropdownMenuItem("Users", href=spa.url_for('admin.users'))
            children.append(users_link)

        children.append(html.Div(className='dropdown-divider'))
        children.append(
            dbc.DropdownMenuItem([html.I(className='fa fa-sign-in'), ' Sign out'], href=spa.url_for('admin.logout'))
        )

        menu = dbc.DropdownMenu(
            children=children,
            nav=True,
            in_navbar=True,
            label="My Account",
            right=True
        )

        icon = html.I(className="fa fa fa-user", style={'position': 'relative','left': '4px'})

        return html.Div(['', icon, menu], style={'padding': '0'}, className='d-flex align-items-center nav-link')

    def signin_link(self):
        return dbc.NavItem(
            dbc.NavLink([html.I(className='fa fa-sign-in'), ' Sign in'], href='/admin/login')
        )

    def layout(self, spa):
        if current_user and not current_user.is_anonymous:
            return self.account_dropdown(spa)
        else:
            return self.signin_link()
