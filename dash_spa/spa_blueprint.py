from utils import log
from urllib import parse
from .spa_components import SpaComponents

class Blueprint(SpaComponents):

    @property
    def name(self):
        return self.io._prefix

    def __init__(self, name):
        super().__init__(name)
        self.spa_app = None
        self.routes = {}

    def route(self, rule, **options):

        class _Route:
            def __init__(self, layout):
                self.__dict__ = options
                self.layout = layout

            def __getattr__(self, name):
                if name in self.__dict__:
                    return self[name]
                else:
                    return None


        def decorator(f):
            log.info('add rule %s%s', self.name, rule)
            self.routes[rule] = _Route(f)
            return f

        return decorator

    def set_spa_app(self, spa_app):
        self.spa_app = spa_app

    def url_for(self, endpoint, args=None):
        """Convert endpoint to url

        Arguments:
            endpoint {str} -- Endpoint to convert

        Keyword Arguments:
            args {dict} -- Arguments to be encoded as a querystring (default: {None})

        Returns:
            str -- The converted endpoint
        """

        def _get_ep():
            nonlocal endpoint
            try:
                ep = self.spa_app.url_for(endpoint)
                return ep
            except Exception:
                pass

            if endpoint and not '.' in endpoint:
                endpoint = '{}.{}'.format(self.name, endpoint)

            return self.spa_app.url_for(endpoint)

        ep = _get_ep()
        if args:
            ep += '?' + parse.urlencode(args)

        return ep
