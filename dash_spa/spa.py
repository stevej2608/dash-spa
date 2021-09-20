import re
import dash_holoniq_components as dhc
from utils import log

import dash
from dash.dependencies import DashDependency
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from .spa_components import SpaComponents

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

    def run_server(self, debug=False, host=None, port=None, threaded=True):
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
        self.dash.layout = self.pageLayout()

    def pageLayout(self):
        """
        Called once on initialisation to provide the top-level page
        layout for the entire application.
        """

        blueprint_routes = self.blueprint_routes
        SHOW_404 = 'show404'

        def page_content_router():
            """Call the layout merthod for each of the registered blueprint routes"""

            page_layouts = {SHOW_404 : self.show404()}

            for route, ctx in self.blueprint_routes.items():
                page_layouts[route] = ctx.layout()

            (routes, children) = zip(*page_layouts.items())
            return dhc.LayoutRouter(children, routes=routes, id='router')

        # Define the dynamic top-level layout components and their
        # associated callback.

        page_content = page_content_router()
        page_title = dhc.PageTitle(title=self.title, id='title')

        @self.dash.callback(page_content.output.switch, page_title.output.title, SpaComponents.url.input.href)
        def _display_page(href):
            route = SHOW_404
            title = SpaComponents.NOUPDATE

            url = SpaComponents.urlsplit(href)

            pathname = re.sub(r"\/$", '', url.path)

            log.info('display_page href=%s', href)

            if pathname and pathname in blueprint_routes:
                route = pathname
                title = blueprint_routes[pathname].title

            return route, title

        # Render the navbar

        navbar = self.navBar(self.navitems) if self.navitems else None

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
            html.Div(id='null')
        ])
        return layout

    def show404(self):
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1('Oops!'),
                        html.H2('404 Not Found'),
                        html.Div('Sorry, an error has occurred, Requested page not found!', className='error-details'),
                        html.Div([

                            dcc.Link([
                                html.Span(className='fa fa-home'),
                                ' Take Me Home'
                            ], href='/', className='btn btn-secondary btn-lg'),

                            dcc.Link([
                                html.Span(className='fa fa-envelope'),
                                ' Contact Support'
                            ], href='/support', className='btn btn-secondary btn-lg'),

                        ], className='error-actions')
                    ], className='error-template')
                ], className='col-md-12')
            ], className='row')
        ], className='container')

    def navBar(self, navitems, dark=True, color='secondary'):
        """Return the navbar for the application"""

        def getItems(items):

            def item(item):

                login_required = item.get('login_required')
                if login_required is not None:
                    if self.user_logged_in() != login_required:
                        return None

                if 'icon' in item:
                    return dbc.NavItem(
                        dbc.NavLink([html.I(className=item['icon']), ' ' + item['title']], href=item["href"])
                    )
                else:
                    return dbc.NavItem(dbc.NavLink(item['title'], href=item["href"]))

            return dbc.Nav([
                item(x) for x in items
            ])

        def navbar_elements():
            items_left = getItems(self.navitems['left'])
            items_right = getItems(self.navitems['right'])
            return [
                dbc.NavbarBrand(html.Strong(navitems['brand']['title']), href="https://datatables.net/"),

                # Left hand side

                dbc.NavItem(items_left, className='navbar-nav mr-auto'),

                # Right hand side

                dbc.NavItem(items_right, className='navbar-nav ml-auto')

            ]

        spa = SpaComponents('navbar')

        navbar = spa.Navbar(children=navbar_elements(),
                id='navbar', className="navbar-default",
                dark=dark, color=color,  expand="md" )

        @self.dash.callback(navbar.output.children, [SpaComponents.url.input.pathname])
        def navbar_cb(pathname):
            children = navbar_elements()
            return children

        return navbar

    def register_blueprint(self, blueprint, url_prefix=None):
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
            full_route = '{}/{}'.format(url_prefix, route.replace('.','/'))
            ep = '{}.{}'.format(blueprint.name, route)
            self.blueprint_routes[full_route] = layout_function
            self.endpoints[ep] = full_route

    def url_for(self, endpoint):
        try:
            return self.endpoints[endpoint] if endpoint else None
        except Exception as ex:
            raise Exception("Unable to resolve endpoint '{}'".format(endpoint)) from ex

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
