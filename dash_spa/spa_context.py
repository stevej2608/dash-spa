import json
from flask import current_app as app
from dash import callback, Output, no_update as NOUPDATE
from dash_prefix import prefix
from dash_spa.logging import log
from dash_redux import ReduxStore
from munch import DefaultMunch

# Provides a React.Js context pattern that allows state to be easily passed
# between components
#
# See examples/react_pattern/pages/context_pattern.py

class State(DefaultMunch):

    def toDict(self):
        _copy = json.loads(json.dumps(self))
        return _copy

class _ContextWrapper:

    @property
    def input(self):
        return self._store.input

    @property
    def output(self):
        return self._store.output

    @property
    def state(self):
        return self._store.state

    def __init__(self, state):
        self._state = state.copy()

    def On(self, *_args, **_kwargs):
        """Transform a @ctx.On(...) callback an @store.update()
        callback on the internal contexts store
        """

        def wrapper(user_func):

            def callback_stub(self, *_args, **_kwargs):
                pass

            if app and app.got_first_request:
                return callback_stub

            log.info("register callback %s", self.id)

            @self._store.update(*_args)
            def _proxy(*_args):
                prev_state = self._state.copy()

                # pop the store reference

                args = list(_args)
                store = args.pop()

                user_func(*args)

                if prev_state != self._state:
                    new_state = self._state.copy()
                    self._state = State.fromDict(new_state)
                    # log.info('Update state %s', new_state)
                    return new_state
                else:
                    return NOUPDATE


        return wrapper

    def Provider(self, state=None, id=id):

        assert id, "The context.Provider must have an id"

        self.id = id
        pid = prefix(id)

        log.info('Provider id=%s', self.id)

        container_id = pid('container')

        # state can be provide when the context is created or passed in here

        self._state = State.fromDict(state.copy() if state is not None else self._state)
        self._store = ReduxStore(id=pid(), data=self._state, storage_type='memory')

        def provider_decorator(func):

            def func_wrapper( *_args, **_kwargs):

                # Call the Dash layout function we've wrapped

                result = func(*_args, **_kwargs)

                result.id = container_id

                # Inject the context store into the layout

                if not isinstance(result.children, list):
                    result.children = [result.children]

                result.children.append(self._store)

                return result

            self.render = func_wrapper

            return func_wrapper

        # Render the container if the context store has been modified

        @callback(Output(container_id, 'children'), self._store.input.data, prevent_initial_call=True)
        def container_cb(store):
            # log.info('Update container %s', container_id)
            container = self.render()
            return container.children

        return provider_decorator

    def useState(self, ref=None, initial_state={}):

        if ref is not None:
            if not ref in self._state:
                self._state[ref] = initial_state.copy()

            state = State(self._state[ref])
        else:
            if not self._state:
                self._state = initial_state.copy()
            state = State(self._state)

        def set_state(state):
            if ref is not None:
                self._state[ref].update(state)
            else:
                self._state.update(state)

        return state, set_state

    def getState(self, ref=None):
        state = self._state[ref] if ref else self._state
        return State(None, state)

    def getStateDict(self, ref=None):
        state = self._state[ref] if ref else self._state
        return state.toDict()


def createContext(state={}):
    return _ContextWrapper(state)

def useContext(ctx: _ContextWrapper):
    return ctx
