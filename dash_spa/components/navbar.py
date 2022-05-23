from dash import html
import dash_bootstrap_components as dbc

from ..spa_pages import DashPage, get_page, add_style

class NavbarBase:

    style = None

    def __init__(self):
        if self.style:
            add_style(self.style)

    def layout(self, spa):
        return None

class NavbarLink(NavbarBase):

    def __init__(self, page: DashPage = None, path: str=None, id = None, login_required=False, icon=None):
        super().__init__()
        if path:
            page = get_page(path)
        self.title = page.short_name or page.title
        self.path=page.path
        self.login_required=login_required
        self.id = id
        self.icon=icon

    def layout(self):
        login_required = self.login_required

        # if login_required and not spa.user_logged_in():
        #     return None

        if self.icon:
            if self.id:
                return dbc.NavItem(
                    dbc.NavLink([html.I(className=self.icon), ' ' + self.title], id=self.id, href=self.path)
                )
            else:
                return dbc.NavItem(
                    dbc.NavLink([html.I(className=self.icon), ' ' + self.title], href=self.path)
                )
        else:
            if self.id:
                return dbc.NavItem(dbc.NavLink(self.title, href=self.path, id=self.id))
            else:
                return dbc.NavItem(dbc.NavLink(self.title, href=self.path))


class NavbarBrand(NavbarBase):

    def __init__(self, title, href):
        super().__init__()
        self.title=title
        self.href=href

    def layout(self):
        text = self.title
        if text:
            return dbc.NavbarBrand(html.Strong(text), href="/", style={"padding-left": ".5rem"})
        else:
            return None

class NavBar:
    """Create the navbar for the application"""

    def __init__(self, navitems, dark=True, color='secondary'):
        self.navitems = navitems
        self.dark = dark
        self.color = color

    def layout(self):
        navitems = self.navitems
        brand = navitems['brand']

        def getItems(items):
            items = items if isinstance(items, list) else [items]
            return dbc.Nav([item.layout() for item in items])

        def navbar_elements():
            items_left = getItems(navitems['left'] if 'left' in navitems else [])
            items_right = getItems(navitems['right'] if 'right' in navitems else [])
            return [
                brand.layout(),

                # Left hand side

                dbc.NavItem(items_left, className='navbar-nav me-auto'),

                # Right hand side

                dbc.NavItem(items_right, className='navbar-nav ms-auto')

            ]

        # Iterate over all navbar element to register any internal callbacks with dash

        elements = navbar_elements()

        # Create navbar

        navbar = dbc.Navbar(children=elements,id='navbar',dark=self.dark, color=self.color,  expand="md" )

        # # Register callback that will update the navbar whenever the browser page changes

        # @self.dash.callback(navbar.output.children, [SpaComponents.url.input.pathname])
        # def navbar_cb(pathname):
        #     children = navbar_elements()
        #     return children

        return navbar
