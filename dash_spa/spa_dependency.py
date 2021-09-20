import re
import dash
from dash.development.base_component import Component
from dash.dependencies import DashDependency

# Simple helper to get the Dash components identifier
#
#   my_checkbox.component_id
#
#   can now be just:
#
#   my_checkbox.id

DashDependency.id = property(lambda self: self.component_id)

class DashIOFactory:
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
        assert hasattr(component, 'id'), "The dash component must have an 'id' attribute"
        self.component = component
        self.iofactory = iofactory


    def is_valid(self, attr):
        if attr not in self.available_properties:
            raise TypeError('`' + self._type + '` has no attribute `' + attr + '`')

    def __getattr__(self, name):
        if not name in self.component.available_properties:
            raise AttributeError(f"'{self.component._type}' component '{self.component.id}' has no attribute '{name}'")

        dio = self.iofactory(self.component.id, name)
        self.__setattr__(name, dio)
        return dio


def input(self):
    if not hasattr(self, '_input'):
        self._input = DashIOFactory(self, dash.dependencies.Input)
    return self._input

def output(self):
    if not hasattr(self, '_output'):
        self._output = DashIOFactory(self, dash.dependencies.Output)
    return self._output

def state(self):
    if not hasattr(self, '_state'):
        self._state = DashIOFactory(self, dash.dependencies.State)
    return self._state

# Inject DashIOFactory instances into the Dash component

Component.input = property(input)
Component.output = property(output)
Component.state = property(state)


def strip(label):
    return re.sub(r"\s+", '_', label).strip().lower()

class SpaDependency:

    # @property
    # def app(self):
    #     return self._spa_components.app

    def __init__(self, prefix):
        self._prefix = strip(prefix)

    def prefix(self, id):
        return f'{self._prefix}-{id}' if id else None

    def copy_factory(self, src, dest):
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
            dest.input.component = src.input.component
            dest.output.component = src.output.component
            dest.state.component = src.state.component

        if hasattr(dest, 'id'):
            _copy()
        else:
            dest.id = src.id + '#container'
            _copy()
            #dest.id = None

        return dest
