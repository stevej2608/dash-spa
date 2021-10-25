import dash
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
from dash import dcc, html
from dash.development.base_component import Component
from holoniq.utils import log

from .spa_components import SpaComponents
from .spa_prefix import copy_factory

def form_prefix(ctx, form_name):
    if form_name is None: form_name = ctx.rule
    prefix = ctx.blueprint.name.replace('.',"-")
    return f'{prefix}-{form_name.lower()}' if form_name else prefix


class SpaForm:

    NOUPDATE = dash.no_update

    def __init__(self, ctx, form_name = None):
        """
        Factory used to quickly create forms

        Usage:

            frm = SpaForm(ctx, 'loginFrm')


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
        self.ctx = ctx
        self.form_name = form_prefix(ctx, form_name)

    def callback(self, output, inputs=[], state=[]):
        """Convenience wrapper for Dash @callback function decorator"""
        return self.ctx.blueprint.callback(output, inputs, state)

    def querystring_args(self, href):
        return self.ctx.querystring_args(href)

    def prefix(self, id):
        if id:
            id = f'{self.form_name}-{id.lower()}'
        return id

    def Form(self, children, id=Component.UNDEFINED, preventDefault=True, **kwargs):
        id = self.prefix(id)
        form = dhc.Form(children, id=id, preventDefault=preventDefault, **kwargs)
        return form

    def Alert(self, message=None, id=Component.UNDEFINED, className="alert alert-danger", **kwargs):
        """Flash"""
        id = self.prefix(id)
        return dhc.Alert(message, id=id, className=className, role="alert", **kwargs)

    def Location(self, id=Component.UNDEFINED, refresh=False, **kwargs):
        """Location"""
        id = self.prefix(id)
        return dhc.Location(id, refresh=refresh, **kwargs)

    def Button(self, label=None, id=Component.UNDEFINED, type='button', className="btn btn-primary", **kwargs):
        """Button"""
        id = self.prefix(id)
        btn = html.Button(label, id=id, type=type, className=className, **kwargs)
        _layout = html.Div(btn, className="d-grid gap-2")
        copy_factory(btn, _layout)
        return _layout


    def Checkbox(self, label=Component.UNDEFINED, id=None, checked=False, **kwargs):
        """Checkbox"""
        id = self.prefix(id)
        checkbox = html.Div([
            dcc.Input(className="form-check-input", id=id, type='checkbox', value=""),
            html.Label(label, htmlFor=id, className="form-check-label")
        ], className='form-check' )
        return checkbox

    def CheckboxX(self, children=None, id=None, checked=False, **kwargs):
        """Checkbox"""
        id = self.prefix(id)

        checkbox = dbc.Checkbox(id=id, className="form-check-input", value=checked, **kwargs)

        # @self.callback(checkbox.output.key, [checkbox.input.value])
        # def _location_cb(checked):
        #     self.value = checked
        #     return SpaForm.NOUPDATE

        _layout = html.Div([
            checkbox,
            dbc.Label(children, html_for=id, className="form-check-label")
        ], className="form-check")



#   <div class="form-check">
#     <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
#     <label class="form-check-label" for="flexCheckDefault">
#         Default checkbox
#     </label>
# </div>

        copy_factory(checkbox, _layout)
        return _layout

    def Input(self, label=None, id=None, type='text', prompt=None, name=None, feedback=None, autoComplete=None, querystring=False, **kwargs):
        """Input"""

        id = self.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback)]
            else:
                return []

        ac = 'on' if autoComplete else None

        _value = None

        input = dbc.Input(id=id, name=name, type=type, autoComplete=ac, value=_value, **kwargs)

        if querystring:

            @self.callback(input.output.value, [SpaComponents.url.input.href])
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

        _layout = html.Div(fields, className='mb-3')

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

    def InputWithIcon(self, label=None, id=None, prompt=None, feedback=None, autoComplete=None, **kwargs):
        """InputWithIcon"""

        id = self.prefix(id)

        def add_feedback():
            if feedback:
                return [dbc.FormFeedback(feedback)]
            else:
                return []

        ac = 'on' if autoComplete else None

        dhc.InputWithIcon(id=id, **kwargs)

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
