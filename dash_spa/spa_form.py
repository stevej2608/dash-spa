from urllib import parse
from argparse import ArgumentError
import dash
from dash import dcc, html
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc

from .callback import callback
from .logging import log

from dash_prefix import prefix, copy_factory, isTriggered

class SpaForm:

    NOUPDATE = dash.no_update

    def __init__(self, form_name = None):
        """
        Factory used to quickly create forms

        Usage:

            frm = SpaForm('loginFrm')


            flash = frm.Alert(id='flash')

            code = frm.Input(name='code', placeholder="verification code", prompt="Check your email in-box")

            button = frm.Button('Submit', type='submit')

            redirect = frm.Location(id='redirect', refresh=True)


            form = frm.Form([
                flash,
                code, html.Br(),
                button,
                registerLink()
            ], id='verify')

        """
        self.prefix = prefix(form_name)

    def Form(self, children, id=Component.UNDEFINED, preventDefault=True, **kwargs):
        id = self.prefix(id)
        form = dhc.Form(children, id=id, preventDefault=preventDefault, **kwargs)
        return form

    def Store(self, form, id='store', fields=None, storage_type='session'):
        """Create  presistent store for the fields in the given form

        Args:
            form (dhc.Form): The form to persist
            id (str, optional): ID of the store. Defaults to 'store'.
            fields (List, optional): Fields to persist. If None, all fields will be persisted
            storage_type (str, optional): Type of storage: local' or 'session' or 'memory. Defaults to 'session'.

        Returns:
            _type_: _description_
        """

        # TODO: Can this be achieved with input persistence?


        id = self.prefix(id)
        store = dcc.Store(id=id, storage_type=storage_type)

        @callback(store.output.data, form.input.form_data)
        def _form_store_cb(values):
            log.info('_form_store_cb values=%s', values)
            if isTriggered(form.input.form_data):
                if fields:
                    data = {}
                    for f in fields:
                        data[f] = values.pop(f, None)
                    return data
                else:
                    return values

            else:
                return SpaForm.NOUPDATE

        return store

    def Alert(self, message=None, id=Component.UNDEFINED, className="alert alert-danger", **kwargs):
        """Flash"""
        id = self.prefix(id)
        return dhc.Alert(message, id=id, className=className, role="alert", **kwargs)

    def Location(self, id=Component.UNDEFINED, refresh=False, **kwargs):
        """Location"""
        id = self.prefix(id)
        return dhc.Location(id=id, refresh=refresh, **kwargs)

    def Button(self, label=None, id=Component.UNDEFINED, type='button', className="btn btn-secondary", **kwargs):
        """Button"""
        id = self.prefix(id)
        btn = html.Button(label, id=id, type=type, className=className, **kwargs)
        _layout = html.Div(btn, className="d-grid gap-2")
        copy_factory(btn, _layout)
        return _layout

    def CheckboxX(self, label=Component.UNDEFINED, id=None, name=None, checked=False, **kwargs):
        """Checkbox"""
        id = self.prefix(id)
        input = dbc.Checkbox(label=label, value=checked, id=id, name=name, **kwargs)
        return input


    def Checkbox(self, label=Component.UNDEFINED, id=None, name=None, checked=False, **kwargs):
        """Checkbox"""
        id = self.prefix(id)

        if isinstance(label, str):
            input = dbc.Checkbox(label=label, value=checked, id=id, name=name, **kwargs)
            return input

        # The standard dbc.Checkbox does not allow html child components in the label
        # attribute. The following composite uses the same markup as dbc.Checkbox and does
        # allow html children. Unfortunately setting the checkbox initial state
        # to True does not work.
        #
        # See: Standalone checkboxes, toggle switches and radio buttons
        # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/input/

        if checked:
            raise ArgumentError('Checkbox: None string lables combined with checked=True is not supported')

        # input = dbc.Input(id=id, name=name, className='form-check-input', type='checkbox')
        # _layout = html.Div([
        #         input,
        #         html.Label(label, className='form-check-label', htmlFor=id)
        #     ], className='form-check')

        style = {'padding': '0 0'}
        input = dbc.Input(id=id, name=name, className='form-check-input', type='checkbox', style=style)
        _layout = html.Div([
                input,
                html.Label(label, className='form-label', htmlFor=id)
            ], className='form-check')

        _layout.name=name

        copy_factory(input, _layout)
        return _layout

    def Input(self, label=None, id=None, type='text', prompt=None, name=None, feedback=None, autoComplete=None, value=None, **kwargs):
        """Input"""

        id = self.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback)]
            else:
                return []

        ac = 'on' if autoComplete else None

        input = dbc.Input(id=id, name=name, type=type, autoComplete=ac, value=value, **kwargs)

        # if querystring:

        #     @self.callback(input.output.value, [SpaComponents.url.input.href])
        #     def _location_cb(href):
        #         nonlocal _value
        #         log.info('input %s: href=%s (%s)', input.id, href, self.get_pathname())
        #         qs = self.querystring_args(href)
        #         if qs and name in qs:
        #             _value = qs[name][0]

        #         log.info('input %s: value %s', input.id, self.value)

        #         return _value

        fields = [
            input,
        ]

        if label:
            fields.insert(0, dbc.Label(label))

        if prompt:
            fields.append(dbc.FormText(prompt))

        fields += add_feedback()

        _layout = html.Div(fields, className='mb-3')

        _layout.name = input.name

        if id is not None:
            copy_factory(input, _layout)

        return _layout

    def PasswordInput(self, label=None, id=None, prompt=None, feedback=None, autoComplete=None, **kwargs):
        """PasswordWithShow"""

        id = self.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback)]
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

        _layout = html.Div(fields, className='mb-3')

        if id is not None:
            copy_factory(input, _layout)

        return _layout


    def querystring_args(self, href):
        """URL parser
        Arguments:
            href {str} -- The URL to be parsed

        Returns:
            [dict] -- K,V pairs of the query string
        """

        def parse_qs(href):
            query = parse.urlsplit(href).query
            qs = parse.parse_qs(query)
            return qs

        qs = parse_qs(href) if href else None

        for key, value in qs.items():
            if isinstance(value, list) and len(value) == 1:
                qs[key] = value[0]

        return qs
