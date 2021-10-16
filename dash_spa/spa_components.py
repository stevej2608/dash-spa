import re
import dash
import dash_holoniq_components as dhc
from dash import dcc
from dash.development.base_component import Component

class SpaComponents:

    NOUPDATE = dash.no_update
    UNDEFINED = Component.UNDEFINED

    url = dcc.Location(id='spa-url')
    redirect = dhc.Location(id='spa-redirect')

    @classmethod
    def isTriggered(cls, input):
        ctx = dash.callback_context

        if not ctx.triggered: return False

        prop_id = f"{input.id}.{input.component_property}"
        return ctx.triggered[0]['prop_id'] == prop_id

    @classmethod
    def prefix(cls, id):
        if id == cls.UNDEFINED:
            return id

        if isinstance(id, list):
            id = '-'.join(id)

        id = re.sub(r"\s+", '_', id).strip().lower()
        return id
