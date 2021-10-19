import inspect
import dash
from dash.development.base_component import Component
from dash.dependencies import DashDependency
from holoniq.utils import log


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

        def get_prefix():

            log.info('get_prefix(%s)', component.id)

            for frm in inspect.stack()[3:]:

                try:

                    mod_name = inspect.getmodule(frm[0]).__name__

                    if mod_name in ['dash_spa.spa', '__main__', '_pytest.python']: break

                    if mod_name in ['dash_spa.spa_prefix']: continue

                    log.info('    Inspecting module %s', inspect.getmodule(frm[0]).__name__)

                    # Use blueprint rule context has been defined

                    if 'ctx' in frm.frame.f_locals:
                        ctx = frm.frame.f_locals['ctx']
                        prefix = ctx.url_prefix[1:].replace('/','-')
                        log.info('       Found prefix %s (ctx.prefix_ids=%s)', prefix, ctx.prefix_ids)
                        return f"{prefix}-{ctx.rule}" if ctx.prefix_ids else None

                except Exception:
                    pass

            # Default to using module name as prefix

            for frm in inspect.stack()[3:]:
                mod = inspect.getmodule(frm[0])
                if mod.__name__  not in  ['dash_spa.spa_prefix','dash_spa.spa_components']:
                    return mod.__name__.replace('.','-')

            raise Exception('Unable to resolve context')


        assert hasattr(component, 'id'), "The dash component must have an 'id' attribute"
        self.component = component

        prefix = get_prefix()

        # We can be called for both input, output and state so we
        # need to avoid adding the prefix more than once

        if prefix and not component.id.startswith(prefix):
            component.id = f"{prefix}-{component.id}"

        if 'container' not in component.id:
            log.info("Resolved id to %s", component.id)

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
        self._spa_input = DashIOFactory(self, dash.dependencies.Input)
    return self._spa_input

def output(self):
    if not hasattr(self, '_spa_output'):
        self._spa_output = DashIOFactory(self, dash.dependencies.Output)
    return self._spa_output

def state(self):
    if not hasattr(self, '_spa_state'):
        self._spa_state = DashIOFactory(self, dash.dependencies.State)
    return self._spa_state

# Inject DashIOFactory instances into the Dash component

Component.input = property(input)
Component.output = property(output)
Component.state = property(state)

def copy_factory(src, dest):
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
