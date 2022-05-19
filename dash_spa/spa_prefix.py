from typing import Callable, Union
import re
import json
import dash
from dash import callback_context, ALL, MATCH, ALLSMALLER
from dash.development.base_component import Component
from dash.dependencies import DashDependency, Input, Output, State

from .component_id import component_id

NOUPDATE = dash.no_update

def isTriggered(component: DashDependency) -> bool:
    """Return true if the given dash component was the reasion for the enclosing callback being triggered

    Args:
        component (DashDependency): The calback component being tested

    Returns:
        bool: Return true if the given component is the trigger
    """
    ctx = callback_context
    if not ctx.triggered:
        return False

    if not hasattr(component,'id'):
        return False

    if isinstance(component.id, dict):
        prop_id = f'{json.dumps(component.id, sort_keys=True, separators=(",", ":"))}.{component.component_property}'
    else:
        prop_id = f'{component.id}.{component.component_property}'

    return ctx.triggered[0]['prop_id'] == prop_id


def trigger_index(idx_field='idx') -> Union[int, None]:
    """Return the index of the match ALL field that triggered the callback

    Args:
        idx_field (str, optional): The MATCH field to test Defaults to 'idx'.

    Returns:
        Union[int, None]: Returns the index or None
    """
    ctx = callback_context
    if ctx.triggered:
        triggered_idx = ctx.triggered_id[idx_field]
        for index, input in enumerate(ctx.inputs_list[0]):
            if triggered_idx == input['id'][idx_field]:
                return index
    else:
        return None


def match(pattern: dict):
    """ Return a match factory that can be used to create
    pattern matching component ids that all use the same base pattern

    Args:
        pattern (dict): Dictionary that contains the base pattern

    Returns:
        _Factory: Factory that creates component IDs based on the supplied pattern

    Example:

            btn = match({'type': 'button', 'idx': ALL})

            btn1 = html.Button(id=btn.idx(1))

            btn2 = html.Button(id=btn.idx(2))

            @app.callback(div.output.children, btn.input.n_clicks)
            def _callback(n_clicks):
                pass

    """

    class _Factory:

        def __init__(self, component_id: dict, dash_factory: DashDependency):
            self.component_id = component_id
            self.dash_factory = dash_factory

        def __getattr__(self, component_property: str) -> DashDependency:
            cb = self.dash_factory(self.component_id, component_property)
            return cb

    class Matcher:
        def __init__(self, pattern: dict):
            self.pattern = pattern

            # For each of the pattern matching dict entries we
            # create a lambda that can be called which in turn
            # calls our resolver method

            def _resolver(key):
                return lambda value : self.resolver(key, value)

            for key, value in pattern.items():

                if key in ['input', 'output', 'state']:
                    raise AttributeError(f'Invalid match key "{key}". Key values "input", "output" and "state" are not allowed')

                if value in [ALL, MATCH, ALLSMALLER]:
                    self.__dict__[key] = _resolver(key)

        def assign(self, **kwargs):
            id = self.pattern.copy()
            for k, v in list(kwargs.items()):
                if k in id and id[k] in [ALL, MATCH, ALLSMALLER]:
                    id[k] = v
                else:
                    raise AttributeError(f'Invalid match key "{k}"')
            return id


        def resolver(self, key: str, value:str) -> dict:
            id = self.pattern.copy()
            id[key] = value
            return id

        def triggerIndex(self):
            ctx = callback_context
            if ctx.triggered:
                id = ctx.triggered[0]['prop_id'].split('.')
                pattern = json.loads(id[0])
                for k,v in self.pattern.items():
                    if v == ALL:
                        return pattern[k]
            return None


        @property
        def input(self) -> _Factory:
            return _Factory(self.pattern, Input)

        @property
        def output(self) -> _Factory:
            return _Factory(self.pattern, Output)

        @property
        def state(self) -> _Factory:
            return _Factory(self.pattern, State)

    return Matcher(pattern)

def prefix(pfx:str = None) -> Callable[[str], str]:
    """Return a lambda that will prefix all component IDs with the
    given prefix. If no prefix is given one will be assigned

    Args:
        pfx (str): The Component prefix to be assigned

    Returns:
         ((str) -> str)


    Example:

    ```
        pid = prefix('test-page')

        btn = html.Button('Hello, id=pid('hello-btn'))
    ```
    """

    def _prefix(pfx, id):
        id = f'{pfx}_{id}' if id else f'{pfx}'
        return id.lower()

    if pfx:
        assert re.search("^[a-zA-Z_]", pfx), "The dash component prefix must start with a letter or underscore"
        pfx = pfx.replace('.', '_')
    else:
        pfx = component_id()

    return lambda id=None : _prefix(pfx, id)


# Simple helper to get the Dash components identifier
#
#   my_checkbox.component_id
#
#   can now be just:
#
#   my_checkbox.id

DashDependency.id = property(lambda self: self.component_id)

class _DashIOFactory:
    """Dash Dependency Factory

Inject DashIOFactory instances into the Dash component. The
factories will be accessable as follows:

    div = html.Div(id='xxx')
    children_attr = div.output.children

Will return the same Dash Dependency Output instance as:

    div = html.Div(id='xxx')
    children_attr = DashDependency.Output('xxx', 'children')

    Raises:
        TypeError: raised id the requested attribute not available on the component
        AttributeError: raised if the associated component has no id

    Returns:
        [obj] -- Dash dependency object Output|Input|State
    """

    def __init__(self, component, iofactory):

        # Add component id prefix if its not allready been done

        if not hasattr(component, '_spa_prefixed_id'):

            assert hasattr(component, 'id'), "The dash component must have an 'id' attribute"

            component._spa_prefixed_id = component.id

        self.component = component
        self.iofactory = iofactory


    def __getattr__(self, name):
        if not name in self.component.available_properties:
            raise AttributeError(f"'{self.component._type}' component '{self.component.id}' has no attribute '{name}'")

        dio = self.iofactory(self.component.id, name)
        self.__setattr__(name, dio)
        return dio


# The following three methods have been injected in to dash's
# Component class as properties 'input', 'output' and 'state'
# In each case, when the property is accessed in a dash callback
# the associated DashIOFactory instance will be invoked

def input(self):
    if not hasattr(self, '_spa_input'):
        self._spa_input = _DashIOFactory(self, dash.dependencies.Input)
    return self._spa_input

def output(self):
    if not hasattr(self, '_spa_output'):
        self._spa_output = _DashIOFactory(self, dash.dependencies.Output)
    return self._spa_output

def state(self):
    if not hasattr(self, '_spa_state'):
        self._spa_state = _DashIOFactory(self, dash.dependencies.State)
    return self._spa_state

Component.input = property(input)
Component.output = property(output)
Component.state = property(state)

def copy_factory(component, composite):
    """Copy Dash I/O Factory

    When a Dash component has been wrapped in additional layout to make
    a composite it is necessary to copy the embedded component I/O definition
    to the outermost component. This will then allow the composite component
    to be referenced in Dash callbacks.

    Arguments:
        src {obj} -- The source Dash component
        dest {obj} -- The destination Dash component

    Returns:
        [Obj] -- The destination component
    """

    def _copy():
        composite.input.component = component.input.component
        composite.output.component = component.output.component
        composite.state.component = component.state.component

    if hasattr(composite, 'id'):
        _copy()
    else:
        composite.id = component.id + '#container'
        _copy()
        #dest.id = None

    return composite

def _css_id(self) -> str:
    """Convert the ID of given Dash component into a css selector

    Args:
        element (Dash element): [description]

    Returns:
        [str]: The component id in a form suitable for use in dash_duo


    Example:

            pid = prefix()

            btn = match({'type': pid('btn'), 'idx': ALL})
            btn1 = html.Button(id=btn.idx(1))

            dash_duo.multiple_click(button1.css_id, clicks=99)

            dash_duo.find_element(btn1.css_id)

    """

    if isinstance(self.id, dict):
        id = json.dumps(self.id, sort_keys=True, separators=(",", ":"))
        for c in r'{}",:':
            id = id.replace(c, f"\\{c}")
    else:
        id = self.id

    return '#' + id

Component.css_id = property(_css_id)
