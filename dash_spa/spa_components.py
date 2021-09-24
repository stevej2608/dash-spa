import inspect
from urllib import parse
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

import dash_holoniq_components as dhc

from utils import log

from .spa_dependency import SpaDependency


class SPAComponent:

    @property
    def layout(self):
        return self._layout


class SpaComponents:
    """
    Factory used to create Dash components that can be referenced in
    callbacks without the need for error prone string references.

    Usage:

        spa = SpaComponents('sector_view')

        sector_title = spa.Div(id='table')

        sector_dropdown = spa.Dropdown(id='trust_sector' ...)

        @app.callback(sector_title.output.children, sector_dropdown.input.value)

        def sector_title_update_cb(selection):
            return html.H2(selection)

    Class Attributes:

        url : Location
            Globally dash Location component

        redirect : Redirect
            Globally available dash Redirect component

        NOUPDATE :
            Default retutn value for callbacks when no updates are required

    """

    url = None
    redirect = None
    NOUPDATE = dash.no_update

    @property
    def app(self):
        return self.parent.app

    def __init__(self, prefix, parent=None):
        """Create SpaComponents using the supplied prefix.

        Factory used to create Dash components that can be referenced in
        callbacks without the need for strings.

        """
        self.io = SpaDependency(prefix)
        self._url_prefix = prefix.split('-')[-1]
        self.parent = parent

        if SpaComponents.url is None:
            SpaComponents.url = dcc.Location(id='spa#url')

        if SpaComponents.redirect is None:
            SpaComponents.redirect = dhc.Location(id='spa#redirect')

    def stack_lookup(self, var):
        for frameinfo in inspect.stack(0):
            if var in frameinfo.frame.f_locals:
                return frameinfo.frame.f_locals[var]
        return None

    def get_context(self):
        return self.stack_lookup('ctx')

    def get_spa(self, prefix=None):
        """Return a new SPAComponent that is a child of this instance

        Arguments:
            prefix {str} -- the postfix to append to the current prefix
        """

        # If prefix is not specified use the blueprint rule. To
        # get this we need to look up the stack to get the blueprint
        # context from spa#pageLayout()

        if prefix is None:
            ctx = self.get_context()
            prefix = ctx.rule.replace('.','-')

        return SpaComponents(f'{self.io._prefix}-{prefix}', self)

        # if prefix is None:
        #     return self
        # else:
        #     return SpaComponents('{}-{}'.format(self.io._prefix, prefix), self)

    def prefix(self, id):
        return self.io.prefix(id)

    def get_pathname(self):
        """Build the canatonical pathname associated with this SpaComponents instance"""

        pathname = (self.parent.get_pathname() + '/' if self.parent else '') + self._url_prefix

        if not pathname.startswith('/'):
            pathname = '/' + pathname
        return  pathname.rstrip('/')

    def set_url_prefix(self, prefix):
        """Set the url_prefix"""
        self._url_prefix = prefix

    def callback(self, output, inputs=[], state=[]):
        """Convenience wrapper for Dash @callback function decorator"""
        return self.parent.callback(output, inputs, state)

    @classmethod
    def urlsplit(cls, href):

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
        if id:
            id = self.prefix(id)
            return html.Button(label, id=id, type=type, className=className, **kwargs)
        else:
            return html.Button(label, type=type, className=className, **kwargs)


    def ButtonLink(self, href='#', id=None, **kwargs):
        """ButtonLink"""

        if id:
            io = self.io
            id = io.prefix(id) if id else None
            return dhc.ButtonLink(id=id, href=href **kwargs)
        else:
            return dhc.ButtonLink(href=href **kwargs)


    def Checkbox(self, children=None, id=None, checked=False, **kwargs):
        """Checkbox"""
        io = self.io
        id = self.prefix(id)
        app = self.app

        checkbox = dbc.Checkbox(id=id, className="form-check-input", checked=checked, **kwargs)

        @app.callback(checkbox.output.key, [checkbox.input.checked])
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

        id = self.prefix(id)
        return dhc.Location(id, refresh=refresh, **kwargs)


    def Dropdown(self, id=None, name=None, **kwargs):
        """[summary]

        Args:
            id (string, optional): ID associated with the component. Defaults to None.
            name (string, optional): Component name. Defaults to None.

        Returns:
            Dropdown: Dash Dropdown component

        """
        io = self.io
        id = io.prefix(id)
        app = self.app

        dropdown = dcc.Dropdown(id=id, **kwargs)
        return dropdown


    def Input(self, label=None, id=None, type='text', prompt=None, name=None, feedback=None, autoComplete=None, querystring=False, **kwargs):
        """Input"""

        io = self.io
        id = io.prefix(id)
        app = self.app

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback, valid=False)]
            else:
                return []

        ac = 'on' if autoComplete else None

        _value = None

        if id:
            input = dbc.Input(id=id, name=name, type=type, autoComplete=ac, value=_value, **kwargs)
        else:
            input = dbc.Input( name=name, type=type, autoComplete=ac, value=_value, **kwargs)

        if querystring:

            @app.callback(input.output.value, [SpaComponents.url.input.href])
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


    def PasswordInput(self, label=None, id=None, prompt=None, feedback=None, autoComplete=None, **kwargs):
        """PasswordWithShow"""

        io = self.io
        id = io.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback, valid=False)]
            else:
                return []

        ac = 'on' if autoComplete else None

        if id:
            input = dhc.PasswordWithShow(id=id, **kwargs)
        else:
            input = dhc.PasswordWithShow(**kwargs)

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

    def InputWithIcon(self, label=None, id=None, prompt=None, feedback=None, autoComplete=None, **kwargs):
        """InputWithIcon"""

        io = self.io
        id = io.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback, valid=False)]
            else:
                return []

        ac = 'on' if autoComplete else None

        if id:
            input = dhc.InputWithIcon(id=id, **kwargs)
        else:
            input = dhc.InputWithIcon(**kwargs)

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
        return dhc.Location(id=io.prefix(id), refresh=refresh, href=href)


    def Navbar(self, children=[], id=None, **kwargs):
        """Navbar"""
        return dbc.Navbar(children, id=self.io.prefix(id), **kwargs)

    def H2(self, children=[], id=None, **kwargs):
        """H2"""
        if id:
            return html.H2(children, id=self.io.prefix(id), **kwargs)
        else:
            return html.H2(children, **kwargs)

    def Flash(self, message=None, id=None, className="alert alert-danger", **kwargs):
        """Flash"""
        io = self.io
        return dhc.Alert(message, id=io.prefix(id), className=className, role="alert", **kwargs)


    def PageTitle(self, title=None, id=None):
        """PageTitle"""
        io = self.io
        return dhc.PageTitle(id=io.prefix(id), title=title)

    @classmethod
    def CallbackContext(cls):
        """Helper to allow the input trigger to be resolved more easily

        The method returns an object the can be used within a callback to
        determin which input triggered the callback execution.

        Usage:

                ctx = SpaComponents.CallbackContext()

                if ctx.isTriggered(sector_dropdown.input.value):
                    ...
                elif ctx.isTriggered(SpaComponents.url.input.href):
                    ...

        """
        ctx = dash.callback_context

        class SpaCallbackContext:

            def isTriggered(self, input):
                """Return true if given input triggered the callback"""

                if not ctx.triggered:
                    return False

                prop_id = f"{input.id}.{input.component_property}"
                return ctx.triggered[0]['prop_id'] == prop_id

        return SpaCallbackContext()
