from typing import Dict, Union, Tuple, Callable, Any, Literal
import sys
import json
from copy import copy
from dash import Output
from dash_prefix import prefix
from dash_spa.logging import log
from dash_spa import callback, NOUPDATE, current_app
from dash_spa.spa_pages import Component
from dash_spa.session import SessionBackendFactory
from dash_spa.utils.caller import caller_hash
from .spa_exceptions import InvalidUsageException
from dash_redux import ReduxStore

from .context_state import ContextState, dataclass, asdict, field, EMPTY_DICT, EMPTY_LIST
from .utils.caller import caller_hash, caller_nested
from dash_spa.logging import log

"""Context state management

ContextState is state/event pattern where a state Context is wrapped by
a @Context.Provider. Dash callback events update the contexts' state which
triggers the method decorated by the @Context.Provider. The decorated
method can then update the Dash UI based on the new context state.

A context can have any number of @Context.Providers. This pattern makes it
possible to create generic Dash components that communicate with host
application via ContextState.

ContextState can, if required, have session persistence.

Example usage:

        @dataclass
        class ButtonState(ContextState):
            clicks: int = 1000

        ButtonContext = createContext(ButtonState)

        def Button(id):
            state = ButtonContext.getState()
            btn = html.Button("Button", id=id)

            @ButtonContext.On(btn.input.n_clicks)
            def btn_click(clicks):
                state.clicks += 1

            return btn


        @ButtonContext.Provider()
        def layout():
            state = ButtonContext.getState()
            btn =  Button(id='test_btn)
            return html.Div(f"button pressed {state.clicks} times!")

"""

@dataclass
class DefaultContext(ContextState):
    __strict__: bool = True

    def items(self):
        fields = []
        for attr in self.__dict__.keys():
            if not attr.startswith("__"):
                field = getattr(self,attr)
                if not callable(field):
                    fields.append(field)
        return fields


# A ReduxStore wrapper that provides a React.Js style context pattern
# that allows a components state change to trigger UI updates.
#
# See examples/context/pages/context_pattern.py
#
# TODO: Is this thread safe?

class Context:

    @property
    def input(self):
        return self._redux_store.input

    @property
    def output(self):
        return self._redux_store.output

    @property
    def state(self):
        return self._redux_store.state


    def input_hash(*_args):

        def unpack(id):

            # Handle dict the keys used by MATCH

            if isinstance(id, dict):
                id = [ part for part in id.values() if isinstance(part, str)]
                return '_'.join(id)
            else:
                return id

        # Create a positive hex hash all the callback inputs

        inputs = []
        for input in _args:
            id = f"{unpack(input.component_id)}.{input.component_property}"
            # log.info('input %s', id)
            inputs.append(id)
        _hash = hash(tuple(inputs))
        _hash += sys.maxsize + 1
        return hex(_hash)[2:]



    def __init__(self, contexts, id, state: ContextState = None):
        self.contexts = contexts
        self.id = id
        self._context_state = state
        self._initial_context_state = {}
        self.allow_initial_state = True

    # def pid(self, id=None):
    #     pfx = prefix(self.id)
    #     return pfx(id)

    def callback(self, *_args, **_kwargs):

        def wrapper(user_func):

            @callback(*_args, self._redux_store.input.data, **_kwargs)
            def _proxy(*_args):
                self.contexts.set_context(self)
                result = user_func(*_args)
                return result

        return wrapper

    def On(self, *_args, **_kwargs):
        """Transform a @ctx.On(...) callback an @store.update()
        callback on the internal contexts store
        """

        def wrapper(user_func):

            def callback_stub(self, *_args, **_kwargs):
                pass

            # if the callback is nested in a callable layout() function
            # then the callback will be instantiated on each layout()
            # execution. We need to guard against submitting the callback
            # more than once.

            if current_app and current_app.is_live:
                return callback_stub

            hash = Context.input_hash(*_args)
            if hash in self._redux_store._surrogate_stores:
                return callback_stub

            # log.info("register callback %s", self.id)

            @self._redux_store.update(*_args)
            def _proxy(*_args):

                try:
                    # pop the store reference

                    args = list(_args)

                    state = args.pop()
                    ref_state = json.dumps(state, sort_keys = True)
                    self._context_state.update(state=state)

                    log.info('******** On Event ***********')
                    log.info('state cid=%s %s', self._context_state.cid(), state)

                    self.contexts.set_context(self)
                    user_func(*args)

                    state = self._context_state.asdict()

                    log.info('state %s', state)

                except Exception as ex:
                    log.warn('Dash/SPA context callback error %s', ex)
                finally:
                    self.contexts.set_context(None)

                # state = self._context_state.asdict()

                if json.dumps(state, sort_keys = True) == ref_state:
                    state = NOUPDATE

                return state


        return wrapper

    def Provider(self, state:ContextState=None, persistent: bool = False):

        if self.id:
            pid = prefix(self.id)
        else:
            pid = prefix(caller_hash(2, "ctx_"))

        # log.info('Provider id=%s', self.id)

        container_id = pid('ctx_container')

        # state can be provide when the context is created or passed in here

        if state == None:
            state = self._context_state

        self._context_state = copy(state)

        # if not persistent:
        #     storage_type = 'memory'
        # else:
        #     storage_type = 'session'

        self._redux_store = ReduxStore(id=pid(), data=state.asdict(), storage_type='memory')

        # The ID passed in is unique, use it to inject a prefix method into the
        # context state. This can then be used create ID's for dash element that are
        # declared in the scope of the active context

        # def pid(id):
        #     return self.pid(id)

        self._context_state.pid = pid

        def provider_decorator(func):

            def func_wrapper( *_args, **_kwargs):

                # Call the Dash layout function we've wrapped

                try:
                    self.contexts.set_context(self)
                    result = func(*_args, **_kwargs)

                    assert isinstance(result, Component), "Methods wrapped with @Context.Provider must return a single dash.Component"

                    result.id = container_id

                    # Inject the context store into the layout

                    if not isinstance(result.children, list):
                        result.children = [result.children]

                    # log.info('store initial_state = %s', self._store.data)

                    # The context may have changed during the update. We
                    # need to copy the state across to the Redux store data

                    self._redux_store.data.update(self._context_state.asdict())
                    result.children.append(self._redux_store)
                except Exception as ex:
                    log.exception('Dash/SPA layout error %s', ex)
                    result = NOUPDATE
                finally:
                    self.allow_initial_state = False
                    self.contexts.set_context(None)

                return result

            self.render = func_wrapper

            # The context provider state is stored in the browser using a ReduxStore. Any
            # dash events from components that are defined in the provider markup update
            # the redux store. The store update generates an event & callback containing the latest
            # state. This is loaded into the provider context and the layout() method is called.
            #
            # Because the provider context state is held in the browser, this mechanism works
            # for multiple context instances on multiple simultaneous browser sessions.
            #
            # There is a gotcha. When a page containing context provider(s) is re-rendered following
            # a page refresh, via browser history for instance, the context state used for the refresh
            # will be a stale, probably from a browser different session.
            #
            # To counter this we store the context state here, on completion of a valid
            # render, into the server-side session storage. When a page is refreshed from the
            # browser history the state is restored from the server-side session prior to calling
            # the layout.

            def session_restore(*_args, **_kwargs):
                nonlocal persistent

                cache = SessionBackendFactory.get_cache()

                log.info('Using cache id=%s', cache.session_id)

                state = cache.get(self.id)

                if state == {} or not persistent :
                    log.info('Restore state %s from _initial_context_state', self.id)
                    state = self._initial_context_state


                self._context_state.update(state=state)

                result = func_wrapper(*_args, **_kwargs)

                cache.set(self.id, self._context_state.asdict())

                # We've just returned from the Dash layout

                if self._initial_context_state == {}:

                    # This must be the first time the Dash layout() function
                    # has been called save a copy of the context state

                    self._initial_context_state = self._context_state.asdict()
                    log.info('Save initial state id=%s %s', self.id, self._initial_context_state)

                return result

            return session_restore

        # Render the container if the context store has been modified

        @callback(Output(container_id, 'children'), self._redux_store.input.data, prevent_initial_call=True)
        def container_cb(state):

            log.info('******** Container render ***********')
            log.info('state %s', state)

            self._context_state.update(state=state)
            self.contexts.set_context(self)

            container = self.render()

            # The context provider state is stored in the browser using a ReduxStore. Any
            # dash events from components that are defined in the provider markup update
            # the redux store. The store update generates an event & callback containing the latest
            # state. This is loaded into the provider context and the layout() method is called.
            #
            # Because the provider context state is held in the browser, this mechanism works
            # for multiple context instances on multiple simultaneous browser sessions.
            #
            # There is a gotcha. When a page containing context provider(s) is re-rendered following
            # a page refresh, via browser history for instance, the context state used for the refresh
            # will be a stale, probably from a browser different session.
            #
            # To counter this we store the context state here, on completion of a valid
            # render, into the server-side session storage. When a page is refreshed from the
            # browser history the state is restored from the server-side session prior to calling
            # the layout.

            log.info('Save state to session store[%s] %s', self.id, state)

            cache = SessionBackendFactory.get_cache()
            cache.set(self.id, self._context_state.asdict())

            return container.children

        return provider_decorator


    def useState(self, ref:str=None, initial_state: ContextState = None) -> Tuple[ContextState, Callable[[Any], None]]:
        """Return the current context state

        Args:
            ref (str, optional): return partial state indexed by ref. Defaults to None.
            initial_state (ContextState, optional): initialise the state prior to return. Defaults to None.

        Returns:
            Tuple[ContextState, Callable[[Any], None]]: The requested state and a setter function

        Note: initial_state value, if present, is only actioned on the first layout call. On following
        calls the initial_state value is ignored. Alternatively, use the getState(update={...})

        The returned tuple contains a callable that is used set the state, if required.

        Example:

            current_page, set_page = TableContext.useState('current_page')

            set_page(99)
        """

        if initial_state is not None and self.allow_initial_state:
            self._context_state.update(ref, initial_state)

        def set_state(state):
            setattr(self._context_state, ref, state)

        if ref is not None:
            state = getattr(self._context_state, ref)
        else:
            state = self._context_state


        return state, set_state


    def getState(self, ref:str=None, update:Union[ContextState, dict]=None) -> ContextState:
        """Get current the context state

        Args:
            ref (str, optional): offset into the context. Defaults to None.
            update (Union[ContextState, dict], optional): Update the state with given values prior to return. Defaults to None.

        Returns:
            ContextState: The current context, updated as required
        """
        if ref is not None:
            state = getattr(self._context_state, ref, update)
        else:
            state = self._context_state

        if update:
            state.update(state=update)


        return state

    def getStateDict(self, ref:str=None) -> dict:
        state = self._context_state[ref] if ref else self._context_state
        return state.asdict().copy()

_NO_CONTEXT_ERROR = "Context can only be used within the scope of a provider"

@dataclass
class ContextWrapper:
    """Interface that maps the global context onto the active context.

    The active context is in set by the @<context>.Provider() and remains
    active until the decorated method returns. The active context is
    switched prior to invoking a callback so the callback executes in
    the context that was active when it was created.

    """

    # TODO: Add global lock to stop context being switched mid update

    dataclass: ContextState
    ctx_lookup : Dict[str, Context] = EMPTY_DICT
    ctx: Context = None

    @property
    def store(self):
        return self.ctx

    def get_context(self, id):
        return self.ctx_lookup[id]

    def get_context_state(self, id):
        return self.ctx_lookup[id]._context_state

    def set_context(self, ctx):
        self.ctx = ctx

    def callback(self, *_args, **_kwargs):
        assert self.ctx, _NO_CONTEXT_ERROR
        return self.ctx.callback(*_args, **_kwargs)

    def On(self, *_args, **_kwargs):
        assert self.ctx, _NO_CONTEXT_ERROR
        return self.ctx.On(*_args, **_kwargs)

    def Provider(self, id:str=None, state:ContextState=None, persistent: bool = True):
        """Dash Layout function decorator

        Args:
            id (str, optional): id of session data. Defaults to hash derived from module.line_number.
            state (ContextState, optional): The state to be associated with the context. Defaults to None.
            persistent (bool, optional): Persist the state across sessions. Defaults to True
        """

        # if caller_nested():
        #     raise InvalidUsageException("Provider wrapper can not be used in nested functions")

        if state == None:
            state = self.dataclass()
            state.__strict__ = False

        if not id:
            id = caller_hash(prefix='S')

        if not id in self.ctx_lookup:
            self.ctx_lookup[id] = Context(self, id, state)

        self.ctx = self.ctx_lookup[id]

        return self.ctx.Provider(state, persistent)

    def wrap(self, layout, id):
        """Wrap the given dash layout in this context"""
        # TODO: Add default hash for ID
        return self.Provider(id=id)(layout)()

    def useState(self, ref:str=None, initial_state: ContextState = None) -> Tuple[ContextState, Callable[[Any], None]]:
        """Return the current context state

        Args:
            ref (str, optional): return partial state indexed by ref. Defaults to None.
            initial_state (ContextState, optional): initialise the state prior to return. Defaults to None.

        Returns:
            Tuple[ContextState, Callable[[Any], None]]: The requested state and a setter function

        Note: initial_state value, if present, is only actioned on the first layout call. On following
        calls the initial_state value is ignored. Alternatively, use the getState(update={...})

        The returned tuple contains a callable that is used set the state, if required.

        Example:

            current_page, set_page = TableContext.useState('current_page')

            set_page(99)

        """
        assert self.ctx, _NO_CONTEXT_ERROR
        return self.ctx.useState(ref, initial_state)

    def getState(self, ref:str=None, update: Union[ContextState, dict]=None) -> ContextState:
        """Get current the context state

        Args:
            ref (str, optional): offset into the context. Defaults to None.
            update (Union[ContextState, dict], optional): Update the state with given values prior to return. Defaults to None.

        Returns:
            ContextState: The current context, updated as required
        """
        assert self.ctx, _NO_CONTEXT_ERROR
        return self.ctx.getState(ref, update)

    def getStateDict(self, ref:str=None) -> dict:
        assert self.ctx, _NO_CONTEXT_ERROR
        return self.ctx.getStateDict(ref)


def createContext(state: ContextState = DefaultContext) -> ContextWrapper:
    return ContextWrapper(state)
