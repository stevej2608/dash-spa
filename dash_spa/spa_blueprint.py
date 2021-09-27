from flask.cli import AppGroup
from urllib import parse
from .spa_components import SpaComponents


class BlueprintAppGroup(AppGroup):
    """Flag cli commands are defined by blueprint"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hasCommand = False

    def command(self, *args, **kwargs):
        self.hasCommand = True
        return super().command(*args, **kwargs)

class Blueprint(SpaComponents):

    @property
    def name(self):
        return self.io._prefix

    @property
    def app(self):
        return self.spa_app.dash

    def __init__(self, name):
        super().__init__(name)
        self.spa_app = None
        self.routes = {}
        self.cli = BlueprintAppGroup(name)

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

        endpoint = route2ep(route)

        class _Route:
            def __init__(self, layout):
                self.__dict__ = options
                self.layout = layout
                self.rule = endpoint
                self.title = title
                self.url = None
                self.callback_context = SpaComponents.CallbackContext()

            def isTriggered(self,input):
                return self.callback_context.isTriggered(input)

            def __getattr__(self, name):
                if name in self.__dict__:
                    return self[name]
                else:
                    return None

            def get_url_query_values(self, id):
                """[summary]

                Args:
                    id (string): The is if the required sq params

                Returns:
                    [list]: List of values for given id
                """
                try:
                    qs = self.url.qs
                    if id in qs:
                        return qs[id][0].split()
                except Exception as ex:
                    return None

        def decorator(f):
            self.routes[endpoint] = _Route(f)
            return f

        return decorator

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

        if not self.spa_app.is_initialisation_completed:
            return self.app.callback(output, inputs, state)
        else:
            return callback

    def set_spa_app(self, spa_app):
        # log.info('set_spa_app %s', self.url_pathname)
        self.spa_app = spa_app

    def mypath(self):
        """Return the full path for the enclosing blueprint endpoint.

        If called outside of a rule context the path of the bluprint is returned.

        Example: The path returned for the blueprint rule '/profile' when the
        blueprint registered as '/user' will be '/user/profile'
        """
        ctx = self.get_context()
        return self.url_for(ctx.rule)

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
