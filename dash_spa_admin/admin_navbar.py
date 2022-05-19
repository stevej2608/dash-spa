from abc import abstractmethod
from flask import current_app as app
from dash_spa import current_user
from dash import html
import dash_bootstrap_components as dbc

from .views.common import LOGIN_ENDPOINT, LOGOUT_ENDPOINT, USERS_ENDPOINT, REGISTER_ADMIN_ENDPOINT

class AdminNavbarComponent:

    def __init__(self):
        pass

    @abstractmethod
    def menu_items(self):
        """User defined components for NavBar My Account dropdown"""
        return [
            dbc.DropdownMenuItem("Messages", href="#"),
            dbc.DropdownMenuItem("Settings", href="#"),
        ]

    def account_dropdown(self):

        children = self.menu_items()

        if app.login_manager.isAdmin():
            users_link = dbc.DropdownMenuItem("Users", href=app.login_manager.path_for(USERS_ENDPOINT))
            children.append(users_link)

        children.append(html.Div(className='dropdown-divider'))
        children.append(
            dbc.DropdownMenuItem([html.I(className='fa fa-sign-in'), ' Sign out'], href=app.login_manager.path_for(LOGOUT_ENDPOINT))
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
        try:
            if app.login_manager.user_count() > 0:
                href=app.login_manager.path_for(LOGIN_ENDPOINT)
            else:
                href=app.login_manager.path_for(REGISTER_ADMIN_ENDPOINT)
            return dbc.NavItem(dbc.NavLink([html.I(className='fa fa-sign-in'), ' Sign in'], href=href))
        except:
            return html.Div('')



    def layout(self, **kwargs):
        if current_user and not current_user.is_anonymous:
            return self.account_dropdown()
        else:
            return self.signin_link()

