import re
from urllib import parse
from dash.development.base_component import Component

from .spa_components import SpaComponents
from .spa_url import SpaURLParse
from .spa_blueprint_app_group import BlueprintAppGroup

class Blueprint:

    @property
    def name(self):
        return self._name

    @property
    def app(self):
        return self.spa_app.dash

    def __init__(self, name):
        self._name = name
        self._url_prefix = None
        self.spa_app = None
        self.routes = {}
        self.cli = BlueprintAppGroup(name)

    def set_url_prefix(self, prefix):
        """Set the url_prefix"""
        self._url_prefix = prefix

    def route(self, route='', title=None, **options):
        """Define Dash/SPA endpoint

        Args:
            route (string): Endpoint defined 'user/profile/name'

            title (string): String that will appear in the browser tab title

            options (dict): Additional option that will be passed to the associated layout

        Maps given endpoint to Dash layout method. The given route will be tagged to the end
        of the associated blueprint name and blueprint registration name.

        Example:

            user = Blueprint('user')

            @user.route('/profile/address', title='Profile')

            def _profile(**options):
                pass

            ...

            spa.register_blueprint(user, url_prefix='/lab15')


            The resulting fully expanded URL will be:

                    /lab15/user/profile/address
        """

        def route2ep(str):
            """Replace '/one/two/three' => 'one.two.three'"""

            if str == '/':
                return ''

            str = str[1:] if str[0] == '/' else str
            str = str[:-1] if str[-1] == '/' else str
            str = str.replace('/', '.')
            return str

        # TODO: I think endpoint should include the blueprint name
        # TODO: Rationalise _Route properties

        endpoint = route2ep(route)
        blueprint = self

        if 'prefix_ids' not in options:
            options['prefix_ids'] = True

        # An instance of _RouteContext is available to the user if the
        # ctx patameter is defined in the Dash/SPA root function

        class _RouteContext:
            def __init__(self, layout):
                self.__dict__ = options
                self.layout = layout
                self.rule = endpoint
                self.title = title
                self.url = None
                self.blueprint = blueprint

            def querystring_args(self, href):
                url_parse = SpaURLParse(self)
                return url_parse.querystring_args(href)

            def prefix(self, id):
                if id == Component.UNDEFINED: return id
                return SpaComponents.prefix([blueprint.name, self.rule, id])

            def callback(self, output, inputs=[], state=[]):
                return blueprint.callback(output, inputs, state)

            def isTriggered(self,input):
                return SpaComponents.isTriggered(input)

            def get_url_query_values(self, qid):
                try:
                    qs = self.url.qs
                    if qid in qs:
                        return qs[qid][0].split()
                except Exception as ex:
                    pass

                return None

            def __getattr__(self, name):
                if name in self.__dict__: return self[name]
                return None

        def decorator(f):
            self.routes[endpoint] = _RouteContext(f)
            return f

        return decorator

    def callback(self, output, inputs=[], state=[]):
        return self.spa_app.callback(output, inputs, state)

    def set_spa_app(self, spa_app):
        # log.info('set_spa_app %s', self.url_pathname)
        self.spa_app = spa_app

    def url_for(self, endpoint=None, args=None):
        """Convert endpoint to url

        Arguments:
            endpoint {str} -- Endpoint to convert in dot notation, eg 'admin.verify.user'

        Keyword Arguments:
            args {dict} -- Arguments to be encoded as a querystring (default: {None})

        Returns:
            str -- The converted endpoint, eg '/admin/verify/user'
        """

        for prefix in ['', self.name + '.']:
            try:
                ep = prefix + endpoint
                ep = self.spa_app.url_for(ep)
                if args:
                    ep += '?' + parse.urlencode(args)
                return ep
            except Exception:
                ep = None

        return ep
