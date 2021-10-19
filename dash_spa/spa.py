import re
from abc import abstractmethod

import dash
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
from dash import html
from dash.dependencies import DashDependency
from holoniq.utils import arg_list, log

from .navbar import NavbarBase
from .page_not_found import PageNotFound
from .spa_components import SpaComponents
from .spa_url import urlsplit

DashDependency.id = property(lambda self: self.component_id)

# Dash supports a ''No Update' option on callback outputs, inject __str__() method
# to get it to display correctly when logging

def __no_update_str__(self):
    return 'NOUPDATE'

setattr(dash.dash._NoUpdate, '__str__', __no_update_str__)
setattr(dash.dash._NoUpdate, '__repr__', __no_update_str__)


class Route404(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class SinglePageApp:

    """Wrapper for Dash instance """

    endpoints = {}

    @property
    def is_initialisation_completed(self):
        """Application layout is completed"""
        return self._is_initialisation_completed

    def __init__(self, dash_factory, navitems=None, title='Dash/SPA'):
        """Create instance of Dash/SPA object

        Args:
            dash_factory (func): Factory that returns Dash instance to wrap
            navitems (dict, optional): Optional Navbar definition. Defaults to None.
            title (str, optional): Application title presented in browser page tab. Defaults to 'Dash/SPA'.
        """

        self.dash = dash_factory()
        self.navitems = navitems
        self.title = title
        self.blueprint_routes = {}
        self.endpoints = {}
        self.login_manager = None
        self.page404 = None
        # self.components = SpaComponents('spa')
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

        def get_layout(route_ctx):
            args = arg_list(route_ctx.layout)
            if 'ctx' in args:
                route_ctx.login_manager = self.login_manager
                content = route_ctx.layout(route_ctx)
            else:
                content = route_ctx.layout()
            return content

        blueprint_routes = self.blueprint_routes

        # Iterate over all routes to register callbacks with dash

        for route, route_ctx in blueprint_routes.items():
            get_layout(route_ctx)

        # Define the dynamic top-level layout components and their
        # associated callback.

        page_content = html.Div(id='spa-page_content')
        page_title = dhc.PageTitle(title=self.title, id='spa-title')

        @self.callback(page_title.output.title, page_content.output.children,SpaComponents.url.input.href)
        def _display_page(href):
            title = SpaComponents.NOUPDATE
            page = SpaComponents.NOUPDATE

            url = urlsplit(href)

            pathname = re.sub(r"\/$", '', url.path)

            if pathname is None or pathname == '':
                pathname = '/'

            log.info('display_page href=%s', href)

            try:

                if pathname in blueprint_routes:
                    route_ctx = blueprint_routes[pathname]
                    title = route_ctx.title
                    route_ctx.url = url
                else:
                    raise Route404(f'Unknown route {pathname}')

                # If route has access guard in place call it

                if not route_ctx.access or route_ctx.access(route_ctx):
                    page = get_layout(route_ctx)

            except Exception as ex:
                msg = ex.message if hasattr(ex, 'message') else "???"
                log.info('Error pathname %s : %s', pathname, msg)
                page_content = self.show404(message=msg)

            return title, page

        # Render the navbar

        navbar = self.navBar(self.navitems) if self.navitems else None
        navbar_content = html.Div(navbar, id='spa-navbar_content')

        # @self.callback(navbar_content.output.children, SpaComponents.url.input.href)
        # def _display_navbar(href):
        #     log.info('display_navbar=%s', href)
        #     navbar = self.navBar(self.navitems) if self.navitems else None
        #     return navbar

        # Render the footer        

        footer = self.footer()
        footer_content = html.Div(footer, id='spa-footer_content')            

        # @self.callback(footer_content.output.children, SpaComponents.url.input.href)
        # def _display_footer(href):
        #     log.info('display_footer=%s', href)
        #     footer = self.footer()
        #     return footer

        # Block any further Dash callback registrations

        self._is_initialisation_completed = True

        # Return the top-level page layout

        layout = html.Div([
            SpaComponents.url,
            SpaComponents.redirect,
            page_title,
            navbar_content,
            html.Br(),
            html.Div([
                html.Div([
                    html.Div([], className="col-md-1"),
                    html.Div(page_content, id='page-content', className="col-md-10"),
                    html.Div([], className="col-md-1")
                ], className='row')
            ], className="container-fluid"),
            html.Div(id='null'),
            footer_content
        ])
        return layout

    @abstractmethod
    def footer_text(self):
        return None

    @abstractmethod
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
        container = html.Div(footer.layout(self), id='footer')

        # Register callback that will update the navbar whenever the browser page changes

        @self.dash.callback(container.output.children, [SpaComponents.url.input.pathname])
        def navbar_cb(pathname):
            return footer.layout(self)

        return container

    @abstractmethod
    def brand_text(self):
        return None

    @abstractmethod
    def brand(self):
        if self.navitems and 'brand' in  self.navitems:
            return self.navitems['brand']
        return NavbarBase()

    @abstractmethod
    def show404(self, message):
        if not self.page404:
            self.page404 = PageNotFound()
        return self.page404.layout(self, message=message)

    @abstractmethod
    def navBar(self, navitems, dark=True, color='secondary'):
        """Return the navbar for the application"""

        brand = self.brand()

        def getItems(items):
            return dbc.Nav([item.layout(self) for item in items])

        def navbar_elements():
            items_left = getItems(navitems['left'] if 'left' in navitems else [])
            items_right = getItems(navitems['right'] if 'right' in navitems else [])
            return [
                brand.layout(self),

                # Left hand side

                dbc.NavItem(items_left, className='navbar-nav mr-auto'),

                # Right hand side

                dbc.NavItem(items_right, className='navbar-nav ml-auto')

            ]

        # Iterate over all navbar element to register any internal callbacks with dash

        elements = navbar_elements()

        # Create navbar

        navbar = dbc.Navbar(children=elements,id='navbar',dark=dark, color=color,  expand="md" )

        # Register callback that will update the navbar whenever the browser page changes

        @self.dash.callback(navbar.output.children, [SpaComponents.url.input.pathname])
        def navbar_cb(pathname):
            children = navbar_elements()
            return children

        return navbar

    def callback(self, output, inputs=[], state=[]):
        """Convenience wrapper for Dash @callback function decorator

        We override the base class callback() to map onto the actual
        dash callback method.
        """

        # Dash callbacks can be defined in the SPA application
        # layout methods. These methods are called on startup and
        # during the normal running of the Dash application. Dash
        # only allows callbacks to be registered on start up so
        # we need to block any repeats that may occur during
        # normal running.

        def callback(self, *_args, **_kwargs):
            pass

        if not self.is_initialisation_completed:
            return self.dash.callback(output, inputs, state)

        return callback

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

            layout_function.url_prefix  = url_prefix

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
