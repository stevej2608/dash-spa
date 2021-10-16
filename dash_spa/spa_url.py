from urllib import parse

def urlsplit(href):

    class URL:
        def __init__(self):
            self.url = parse.urlsplit(href)

            query = parse.urlsplit(href).query
            self.qs = parse.parse_qs(query)

            path = self.url.path.decode("utf-8") if isinstance(self.url.path, bytes) else self.url.path

            if href:
                tmp = path[1:] if path.startswith('/') else path
                self.paths = tmp.split('/')
            else:
                self.paths = []

            self.path = path


        @property
        def path_last(self):
            return self.paths[-1]

    return URL()

class SpaURLParse:

    def __init__(self, ctx):
        self.ctx = ctx

    def get_pathname(self):
        pathname = f'{self.ctx.url_prefix}/{self.ctx.rule}'
        if not pathname.startswith('/'):
            pathname = '/' + pathname
        return  pathname.rstrip('/')


    def querystring_args(self, href):
        """URL parser

        The parser returns `None` if the last element of the URL path does not
        match the spa prefix that was passed when the SpaDependency instance
        was created. Assuming the prefix matches then the URL query string is
        returned as a dictionary

        Arguments:
            href {str} -- The URL to be parsed

        Returns:
            [dict] -- K,V pairs of the query string
        """
        results = None
        if href:
            url = urlsplit(href)
            if url.path == self.get_pathname():
                results = url.qs
        return results
