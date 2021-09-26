from dash import html
import dash_bootstrap_components as dbc

class NavbarBase:

    def layout(self, spa):
        return None

class NavbarLink(NavbarBase):

    def __init__(self, title, href, login_required=False, icon=None):
        self.title=title
        self.href=href
        self.login_required=login_required
        self.icon=icon

    def layout(self, spa):
        login_required = self.login_required

        if login_required and not spa.user_logged_in():
            return None

        if self.icon:
            return dbc.NavItem(
                dbc.NavLink([html.I(className=self.icon), ' ' + self.title], href=self.href)
            )
        else:
            return dbc.NavItem(dbc.NavLink(self.title, href=self.href))


class NavbarBrand(NavbarBase):

    def __init__(self, title, href):
        self.title=title
        self.href=href

    def layout(self, spa):
        text = spa.brand_text() or self.title
        if text:
            return dbc.NavbarBrand(html.Strong(text,self.href))
        else:
            return None

class Footer(NavbarBase):

    def __init__(self, title=None):
        self.title=title

    def layout(self, spa):
        text = spa.footer_text() or self.title
        if text:
            return html.Footer([
                html.Div([
                    html.P(text, className='text-center font-italic', style={'marginTop': 10})
                ], className='containers')
            ], className='footer')
        else:
            return None
