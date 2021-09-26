import re

from utils import log, arg_list

import dash
from dash import html
from dash.dependencies import DashDependency
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc

from .spa_components import SpaComponents

from .page_not_found import PageNotFound
from .navbar import NavbarBase

DashDependency.id = property(lambda self: self.component_id)

# Dash supports a ''No Update' option on callback outputs, inject __str__() method
# to get it to display correctly when logging

def __no_update_str__(self):
    return 'NOUPDATE'

setattr(dash.dash._NoUpdate, '__str__', __no_update_str__)
setattr(dash.dash._NoUpdate, '__repr__', __no_update_str__)

class SinglePageApp:

    """Wrapper dor Dash instance """

    endpoints = {}

    @property
    def is_initialisation_completed(self):
        """Application layout is completed"""
        return self._is_initialisation_completed

    def __init__(self, dash, navitems=None, title='Dash/SPA'):
        """Create instance of Dash/SPA object

        Args:
            dash (dash.Dash): Dash instance to wrap
            navitems (dict, optional): Optional Navbar definition. Defaults to None.
            title (str, optional): Application title presented in browser page tab. Defaults to 'Dash/SPA'.
        """
        self.dash = dash
        self.navitems = navitems
        self.title = title
        self.blueprint_routes = {}
        self.endpoints = {}
        self.login_manager = None
        self.page404 = None
        self.components = SpaComponents('spa')
        self._is_initialisation_completed = False

    def run_server(self, debug=False, host='localhost', port=5000, threaded=True):
        """Start the Dash/SPA server

        Args:
            debug (bool, optional): Enable Dash debugging. Defaults to False.
            threaded (bool, optional): Enable threading. Defaults to True.
        """

        if not self.dash.layout:
            self.dash.layout = self.pageLayout()

        if debug:
            self.dash.run_server(debug=debug, host=host, port=port, threaded=threaded, dev_tools_serve_dev_bundles=True)
        else:
            self.dash.run_server(debug=debug, host=host, port=port, threaded=threaded)

    def layout(self):
        """Layout the Dash/SPA application"""
        self.dash.layout = self.pageLayout()

    def pageLayout(self):
        """
        Called once on initialisation to provide the top-level page
        layout for the entire application.
        """

        def get_content(ctx):
            args = arg_list(ctx.layout)
            if 'ctx' in args:
                ctx.login_manager = self.login_manager
                content = ctx.layout(ctx)
            else:
                content = ctx.layout()
            return content

        blueprint_routes = self.blueprint_routes

        # Iterate over all routes to register callbacks with dash

        for route, ctx in blueprint_routes.items():
            get_content(ctx)

        # Define the dynamic top-level layout components and their
        # associated callback.

        page_content = html.Div(id='page_content')
        page_title = dhc.PageTitle(title=self.title, id='title')

        @self.dash.callback(page_content.output.children, page_title.output.title, SpaComponents.url.input.href)
        def _display_page(href):
            title = SpaComponents.NOUPDATE

            url = SpaComponents.urlsplit(href)

            pathname = re.sub(r"\/$", '', url.path)

            if pathname is None or pathname == '':
                pathname = '/'

            log.info('display_page href=%s', href)

            if pathname in blueprint_routes:
                ctx = blueprint_routes[pathname]
                title = ctx.title
                ctx.url = url
                content = get_content(ctx)
            else:
                content = self.show404()

            return content, title

        # Render the navbar & footer

        navbar = self.navBar(self.navitems) if self.navitems else None
        footer = self.footer()

        # Block any further Dash callback registrations

        self._is_initialisation_completed = True

        # Return the top-level page layout

        layout = html.Div([
            SpaComponents.url,
            SpaComponents.redirect,
            page_title,
            navbar,
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(page_content, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
            html.Div(id='null'),
            footer
        ])
        return layout

    def footer_text(self):
        return None

    def footer(self):
        """Create footer components and register a Dash callback that will
        update the footer whenever the route changes

        Returns:
            object: The footer container
        """

        # Do nothing if footer is undefined

        if not self.navitems or not 'footer' in  self.navitems:
            return None

        # Create a container for the footer

        footer = self.navitems['footer']
        container = self.components.Div(footer.layout(self), id='footer')

        # Register callback that will update the navbar whenever the browser page changes

        @self.dash.callback(container.output.children, [SpaComponents.url.input.pathname])
        def navbar_cb(pathname):
            return footer.layout(self)

        return container

    def brand_text(self):
        return None

    def brand(self):
        if self.navitems and 'brand' in  self.navitems:
            return self.navitems['brand']
        return NavbarBase()

    def show404(self):
        if not self.page404:
            self.page404 = PageNotFound()
        return self.page404.layout(self)

    def navBar(self, navitems, dark=True, color='secondary'):
        """Return the navbar for the application"""

        brand = self.brand()

        def getItems(items):
            return dbc.Nav([item.layout(self) for item in items])

        def navbar_elements():
            items_left = getItems(self.navitems['left'] if 'left' in self.navitems else [])
            items_right = getItems(self.navitems['right'] if 'right' in self.navitems else [])
            return [
                brand.layout(self),

                # Left hand side

                dbc.NavItem(items_left, className='navbar-nav mr-auto'),

                # Right hand side

                dbc.NavItem(items_right, className='navbar-nav ml-auto')

            ]

        # Create navbar

        navbar = self.components.Navbar(children=navbar_elements(),
                id='navbar',dark=dark, color=color,  expand="md" )

        # Iterate over all navbar element to register any internal callbacks with dash

        navbar_elements()

        # Register callback that will update the navbar whenever the browser page changes

        @self.dash.callback(navbar.output.children, [SpaComponents.url.input.pathname])
        def navbar_cb(pathname):
            children = navbar_elements()
            return children

        return navbar

    def register_blueprint(self, blueprint, url_prefix='/'):
        """Register blueprint with Dash/SPA application

        Args:
            blueprint (dash_spa.Blueprint): The Blueprint being registered
            url_prefix (String, optional): The prefix to be applied to all routes defined by the blueprint. Defaults to None.

        Example:

                admin = Blueprint('admin')

                app = dash.Dash(__name__)
                spa = SinglePageApp(app)

                spa.register_blueprint(admin, url_prefix='/server')

        """

        blueprint.set_url_prefix(url_prefix)
        blueprint.set_spa_app(self)

        # Pass any cli commands across to Flask

        if blueprint.cli.hasCommand:
            self.dash.server.cli.add_command(blueprint.cli)

        # Process endpoints

        for route, layout_function in blueprint.routes.items():

            if route:
                full_route = f"{url_prefix}/{route.replace('.','/')}"
            else:
                full_route = url_prefix

            ep = f'{blueprint.name}.{route}'
            self.blueprint_routes[full_route] = layout_function
            self.endpoints[ep] = full_route

    def url_for(self, endpoint):
        try:
            return self.endpoints[endpoint] if endpoint else None
        except Exception as ex:
            raise Exception(f"Unable to resolve endpoint '{endpoint}'") from ex

    def enable_login_manager(self, login_manager, login_view):

        self.login_manager = login_manager
        self.login_manager.login_view = login_view
        self.login_manager.init_app(self.dash.server)

    def user_logged_in(self):
        """Return True if user is valid and is not anonymouse
        """
        if self.login_manager:
            try:
                user = self.login_manager.reload_user()
                return user and user.is_anonymous is False
            except Exception as ex:
                pass

        return False
