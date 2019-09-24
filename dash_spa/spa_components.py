from functools import wraps

from urllib import parse
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import dash_holoniq_components as dhc

from utils import log

from .spa_dependency import SpaDependency


class SPAComponent:

    @property
    def layout(self):
        return self._layout


class SpaComponents:

    url = None

    NOUPDATE = dash.no_update


    def __init__(self, prefix, parent=None):
        self.io = SpaDependency(prefix)
        self.url_pathname = prefix.split('-')[-1]
        self.parent = parent

        if SpaComponents.url is None:
            SpaComponents.url = self.Location()

    def get_spa(self, prefix):
        """Return a new SPAComponent that is a child of this instance

        Arguments:
            prefix {str} -- the postfix to append to the current prefix
        """
        return SpaComponents('{}-{}'.format(self.io._prefix, prefix), self)


    def prefix(self, id):
        return self.io.prefix(id)

    def get_pathname(self):
        pathname = (self.parent.get_pathname() + '/' if self.parent else '') + self.url_pathname
        if not pathname.startswith('/'):
            pathname = '/' + pathname
        return  pathname.rstrip('/')

    def set_pathname(self, pathname):
        self.url_pathname = pathname

    def callback(self, output, inputs=[], state=[]):
        return self.io.callback(output, inputs, state)

    def urlsplit(self, href):

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
            url = self.urlsplit(href)
            if url.path == self.get_pathname():
                results = url.qs
        return results


    def Form(self, children, id=None, preventDefault=True, **kwargs):
        id = self.prefix(id)
        form = dhc.Form(children, id=id, preventDefault=preventDefault, **kwargs)
        return form


    def Div(self, children=None, **kwargs):
        id = kwargs.get('id', None)
        kwargs['id'] = self.prefix(id)
        return html.Div(children, **kwargs)

    def Null(self):
        id = self.prefix('null')
        return html.Div(id=id)


    def Button(self, label=None, id=None, type='button', className="btn btn-primary btn-block", **kwargs):
        """Button"""
        id = self.prefix(id)
        return html.Button(label, id=id, type=type, className=className, **kwargs)


    def ButtonLink(self, label=None, id=None, **kwargs):
        """ButtonLink"""
        io = self.io
        id = io.prefix(id) if id else None

        if href is None:
            href = '#'

        return dhc.ButtonLink(id=id, **kwargs)


    def Checkbox(self, children=None, id=None, checked=False, **kwargs):
        """Checkbox"""
        io = self.io
        id = self.prefix(id)

        checkbox = dbc.Checkbox(id=id, className="form-check-input", checked=checked, **kwargs)

        @io.callback(checkbox.output.key, [checkbox.input.checked])
        def _location_cb(checked):
            self.value = checked
            return SpaComponents.NOUPDATE

        fields = [
            checkbox,
            dbc.Label(children, html_for=id, className="form-check-label")
        ]

        _layout = dbc.FormGroup(fields, check=True)
        io.copy_factory(checkbox, _layout)
        return _layout


    def Location(self, id=None, refresh=False, **kwargs):
        """Location"""

        id = self.prefix(id) if id else 'spa#root#url'
        return dcc.Location(id, refresh=refresh, **kwargs)


    def Dropdown(self, id=None, name=None, querystring=False, **kwargs):
        """Dropdown"""

        io = self.io
        id = io.prefix(id)

        dropdown = dcc.Dropdown(id=id, **kwargs)

        if querystring:

            @io.callback(dropdown.output.value, [SpaComponents.url.input.href])
            def _location_cb(href):
                value = SpaComponents.NOUPDATE

                log.info('dropdown %s: href=%s (%s)', dropdown.id, href, self.get_pathname())

                qs = self.querystring_args(href)

                if qs is not None:
                    if name in qs:
                        value = self.value = qs[name][0].split()

                return value

        return dropdown


    def Input(self, label=None, id=None, type='text', prompt=None, name=None, feedback=None, autoComplete=None, querystring=False, **kwargs):
        """Input"""

        io = self.io
        id = io.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback, valid=False)]
            else:
                return []

        ac = 'on' if autoComplete else None

        _value = None

        input = dbc.Input(id=id, name=name, type=type, autoComplete=ac, value=_value, **kwargs)

        if querystring:

            @io.callback(input.output.value, [SpaComponents.url.input.href])
            def _location_cb(href):
                nonlocal _value
                log.info('input %s: href=%s (%s)', input.id, href, self.get_pathname())
                qs = self.querystring_args(href)
                if qs and name in qs:
                    _value = qs[name][0]

                log.info('input %s: value %s', input.id, self.value)

                return _value

        fields = [
            input,
        ]

        if label:
            fields.insert(0, dbc.Label(label))

        if prompt:
            fields.append(dbc.FormText(prompt))

        fields += add_feedback()

        _layout = dbc.FormGroup(fields)

        if id is not None:
            io.copy_factory(input, _layout)

        return _layout


    def PasswordInput(self, label, id=None, prompt=None, feedback=None, autoComplete=None, **kwargs):
        """PasswordWithShow"""

        io = self.io
        id = io.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback, valid=False)]
            else:
                return []

        ac = 'on' if autoComplete else None

        input = dhc.PasswordWithShow(id=id, **kwargs)

        fields = [input]

        if label:
            fields.insert(0, dbc.Label(label))

        if prompt:
            fields.append(dbc.FormText(prompt))

        fields += add_feedback()

        _layout = dbc.FormGroup(fields)

        if id is not None:
            io.copy_factory(input, _layout)

        return _layout


    def LayoutRouter(self, children=[], switch=None, routes=[], id=None):
        """LayoutRouter"""
        io = self.io
        return dhc.LayoutRouter(children, id=io.prefix(id), switch=switch, routes=routes)


    def ChildRouter(self, id=None):
        """Encapsulation of the standard Dash mechanism for including dynamic
        layout. New layout is sent to the component's `children` attribute.

        The mechanism has a serious shortcomming in that and callbacks associated
        with the dynamic content will not executed. LayoutRouter may be a better
        alternative.

        Keyword Arguments:
            id {string} -- the components ID (default: {None})

        Returns:
            {obj} -- Component instance with callback I/O helpers
        """
        io = self.io
        return html.Div([], id=io.prefix(id))

    def Redirect(self, id=None, refresh=None, href=None):
        """Redirect"""

        io = self.io
        return dhc.Redirect(id=io.prefix(id), refresh=refresh, href=href)


    def Flash(self, message=None, id=None, className="alert alert-danger", **kwargs):
        """Flash"""
        io = self.io
        return dhc.Alert(message, id=io.prefix(id), className=className, role="alert", **kwargs)


    def PageTitle(self, title=None, id=None):
        """PageTitle"""
        io = self.io
        return dhc.PageTitle(id=io.prefix(id), title=title)
