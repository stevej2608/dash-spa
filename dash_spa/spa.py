from utils import log

import dash
from dash.dependencies import DashDependency
import dash_html_components as html
import dash_core_components as dcc
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

    def __init__(self, _dash, navitems=None, pages=None, title='Dash/SPA'):
        self.dash = _dash
        self.navitems = navitems
        self.title = title
        self.routes = {}
        self.endpoints = {}

    def run_server(self, debug=True, threaded=True):
        self.init()
        self.dash.run_server(debug=debug, threaded=threaded)
        # self.dash.run_server(debug=debug, threaded=threaded, dev_tools_serve_dev_bundles=True)

    def init(self):
        self._layout = self.page_layout()
        self.dash.layout = self.layout
        return self.dash

    def layout(self):
        """Return the dash component tree

        We rebuild the application layout for each refresh. This is
        experimental and may have side effects

        Returns:
            Object -- The root Dash element of a tree of elements
        """

        log.info('SPA: refresh')

        try:

            # Clear the Dash layout & callback state prior rebuilding, it's
            # as if this is the first call prior to calling dash.run_server()


            self.dash.callback_map = {}
            self.dash._layout = None

            # Rebuild everything

            layout = self.page_layout()

        finally:

            # Allow dash to call us again on the next refresh

            self.dash._layout = self.layout

        return layout


    def page_layout(self):
        """layout the application's Dash components

        This method is called by Dash on start-up The applications
        component tree is built and all associated callbacks
        are visited.

        Returns:9
            Object -- The root Dash element of a tree of elements
        """

        spa = SpaComponents('spa')
        _outer = self

        def just_layouts(routes):
            result = {}
            for route, el in routes.items():
                result[route] = el.dash_layout
            return result

        def hash_route(route):
            if route is not None:
                route = route.replace('/', '-')
                return route[1:]
            return None

        # Iterate all registered routes calling the layout
        # function for each route

        routes = {}

        for route, el in self.routes.items():
            try:
                el.dash_layout = el.layout()
                routes[hash_route(route)] = el
            except Exception as ex:
                log.error('Route %s, layout failed: %s', route, ex)
                raise ex

        # Gather the Dash layouts for each of the routes

        layouts = just_layouts(routes)

        # Add an undefined 404 route

        layouts['undefined'] = self.show404()

        (hash_routes, children) = zip(*layouts.items())

        router = spa.LayoutRouter(children, routes=hash_routes, id='router')

        self.page_title = self.title

        title = spa.PageTitle(id='title', title=self.page_title)

        navbar = self.navBar(self.navitems) if self.navitems else None

        @self.dash.callback([router.output.switch, title.output.title], [SpaComponents.url.input.href])
        def _cb_root(href):
            title = spa.NOUPDATE

            url = spa.urlsplit(href)

            pathname = url.path

            log.info('_cb_root[href] %s', pathname)

            hash_pathname = hash_route(pathname)

            if hash_pathname in routes:

                el = routes[hash_pathname]

                if el.login_required:
                    if not self.user_logged_in():
                        login_view = self.login_manager.login_view
                        hash_pathname = self.url_for(login_view)

                if el.anonymouse_only:
                    if self.user_logged_in():
                        hash_pathname = 'undefined'

                if el.validate and not el.validate(href):
                    hash_pathname = 'undefined'


                if el.title:
                    new_title = self.get_title(self.title, el.title)
                    if self.page_title != new_title:
                        title = self.page_title = new_title

            else:
                hash_pathname = 'undefined'

            log.info('router.output.switch: %s title:%s', hash_pathname, title)

            return hash_pathname, title

        # Create the dash layout

        layout = self.page_body(navbar, router)

        layout.children.insert(0, SpaComponents.url)
        layout.children.insert(0, title)

        log.info('SPA: page layout - done')

        return layout

    def get_title(self, title, subtitle):
        return '{}:{}'.format(title, subtitle)

    def page_body(self, navbar, router):
        return html.Div([
            navbar,
            html.Br(),
            html.Div([
                html.Div([
                    html.Div(className="col-md-2"),
                    html.Div(router, className="col-md-8"),
                    html.Div(className="col-md-2")
                ], className='row')
            ], className="container-fluid"),
            html.Div(id='null'),
            self.footer()
        ])

    def footer_text(self):
        return 'Dash/SPA'

    def footer(self):
        return html.Footer([
            html.Div([
                html.P(self.footer_text(), className='text-center font-italic', style={'marginTop': 10})
            ], className='containers')
        ], className='footer')


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
        """Return the navbar layout, constructed from the supplied dictionary definition

        Returns:
            [object] -- Navbar ready for display
        """

        def item(item):

            def ep_split():
                ep = item["endpoint"]
                ep = ep.split('?')
                return ep[0], ep[1] if len(ep) > 1 else None

            endpoint, querystring = ep_split()
            href = self.url_for(endpoint)

            login_required = item.get('login_required')
            if login_required is not None:
                if self.user_logged_in() != login_required:
                    return None

            if querystring:
                href = href + '?' + querystring

            if 'icon' in item:
                return dbc.NavItem([
                    dbc.NavLink([html.I(className=item['icon']), ' ' + item['title']], href=href)
                ])
            else:
                return dbc.NavItem(dbc.NavLink(item['title'], href=href))

        def get_items(side):
            if navitems and side in navitems:
                items = navitems[side]

                return dbc.Nav([
                    item(x) for x in items
                ])
            return None

        def brand():
            if navitems and 'brand' in navitems:
                brand = navitems['brand']
                return dbc.NavbarBrand(html.Strong(brand['title']), href=brand['href'])
            return None

        navbar = dbc.Navbar(
            children=[
                brand(),
                dbc.NavItem(get_items('left'), className='navbar-nav mr-auto'),
                dbc.NavItem(get_items('right'), className='navbar-nav ml-auto')
            ], className="navbar-default", dark=dark, color=color, expand="md")

        return navbar

    def register_blueprint(self, blueprint, url_prefix=None):
        log.info('register_blueprint %s', url_prefix)

        blueprint.set_pathname(url_prefix)
        blueprint.set_spa_app(self)

        for route, layout_function in blueprint.routes.items():

            full_route = url_prefix + route if url_prefix else route

            if full_route.endswith('/'):
                full_route = full_route[:-1]

            if full_route.startswith('//'):
                full_route = full_route[1:]

            ep = blueprint.name + route.replace('/', '.').rstrip('.')
            log.info('route %s', full_route)
            self.routes[full_route] = layout_function
            self.endpoints[ep] = full_route


    def url_for(self, endpoint):
        try:
            return self.endpoints[endpoint] if endpoint else None
        except Exception:
            raise Exception("Unable to resolve endpoint '{}'".format(endpoint))

    def enable_login_manager(self, login_manager, login_view):

        self.login_manager = login_manager
        self.login_manager.login_view = login_view
        self.login_manager.init_app(self.dash.server)

    def user_logged_in(self):
        """Return True if user is valid and is not anonymouse
        """
        log.info('user_logged_in')
        if self.login_manager:
            try:
                user = self.login_manager.reload_user()
                return user and user.is_anonymous is False
            except Exception:
                pass

        return False
