import json
from copy import copy
from flask import current_app as app
from dash import Output
from dataclasses import dataclass
from dash_prefix import prefix
from dash_spa.logging import log
from dash_spa import callback, NOUPDATE
from dash_redux import ReduxStore

from .context_state import ContextState
from dash_spa.logging import log

# A ReduxStore wrapper that provides a React.Js style context pattern
# that allows a components state change to trigger UI updates.
#
# See examples/context/pages/context_pattern.py
#
# TODO: Is this thread safe?

class _Context:

    @property
    def input(self):
        return self._store.input

    @property
    def output(self):
        return self._store.output

    @property
    def state(self):
        return self._store.state

    def __init__(self, contexts, id, state: ContextState = None):
        self.contexts = contexts
        self.id = id
        self._state = state

    def callback(self, *_args, **_kwargs):

        def wrapper(user_func):

            @callback(*_args, self._store.input.data, **_kwargs)
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

            if app and app.got_first_request:
                return callback_stub

            # log.info("register callback %s", self.id)

            @self._store.update(*_args)
            def _proxy(*_args):

                # pop the store reference

                args = list(_args)

                state = args.pop()
                ref_state = json.dumps(state, sort_keys = True)
                self._state.map_store(state)

                log.info('******** On Event ***********')
                log.info('state %s', state)

                self.contexts.set_context(self)

                user_func(*args)

                log.info('state %s', state)

                if json.dumps(state, sort_keys = True) == ref_state:
                    new_state = NOUPDATE

                return state


        return wrapper

    def Provider(self, state:ContextState=None, id=id):

        assert id, "The context.Provider must have an id"

        self.id = id
        pid = prefix(id)

        # log.info('Provider id=%s', self.id)

        container_id = pid('container')

        # state can be provide when the context is created or passed in here

        self._state = copy(state) if state is not None else self._state
        self._store = ReduxStore(id=pid(), data=self._state.state, storage_type='session')

        def provider_decorator(func):

            def func_wrapper( *_args, **_kwargs):

                # Call the Dash layout function we've wrapped

                self.contexts.set_context(self)
                result = func(*_args, **_kwargs)

                result.id = container_id

                # Inject the context store into the layout

                if not isinstance(result.children, list):
                    result.children = [result.children]

                # log.info('store initial_state = %s', self._store.data)

                # The context may have changed during the update. We
                # need to copy the state across to the Redux store data

                self._store.data.update(self._state.state)
                result.children.append(self._store)

                return result

            self.render = func_wrapper

            return func_wrapper

        # Render the container if the context store has been modified

        @callback(Output(container_id, 'children'), self._store.input.data, prevent_initial_call=True)
        def container_cb(state):

            log.info('******** Container render ***********')
            log.info('state %s', state)

            self._state.map_store(state)
            self.contexts.set_context(self)

            container = self.render()

            return container.children

        return provider_decorator


    def useState(self, ref=None, initial_state: ContextState = None):
        if initial_state is not None:
            self._state.update(ref, initial_state)

        def set_state(state):
            self._state.update(ref, state)

        if ref is not None:
            state = getattr(self._state, ref)
        else:
            state = self._state

        return state, set_state


    def getState(self, ref=None):
        if ref is not None:
            state = getattr(self._state, ref)
        else:
            state = self._state
        return state

    def getStateDict(self, ref=None):
        state = self._state[ref] if ref else self._state
        return state.copy()


class _ContextWrapper:
    """Interface that maps the global context onto the active context.

    The active context is in set by the @<context>.Provider() and remains
    active until the decorated method returns. The active context is
    switched prior to invoking a callback so the callback executes in
    the context that was active when it was created.

    """

    def __init__(self, state: ContextState):
        self.ctx = None
        self.state_dataclass = state

    def set_context(self, ctx):
        self.ctx = ctx

    def callback(self, *_args, **_kwargs):
            return self.ctx.callback(*_args, **_kwargs)

    def On(self, *_args, **_kwargs):
        return self.ctx.On(*_args, **_kwargs)

    def Provider(self, id=id, state:ContextState=None):
        state = state if state else self.state_dataclass()
        self.ctx = _Context(self, id, state)
        return self.ctx.Provider(state, id)

    def useState(self, ref=None, initial_state: ContextState = None):
        return self.ctx.useState(ref, initial_state)

    def getState(self, ref=None):
        return self.ctx.getState(ref)

    def getStateDict(self, ref=None):
        return self.ctx.getStateDict(ref)

def createContext(state: ContextState = None) -> _ContextWrapper:
    return _ContextWrapper(state)

# def useContext(ctx: _ContextWrapper):
#     return ctx
