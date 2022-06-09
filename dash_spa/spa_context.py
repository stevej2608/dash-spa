from typing import TypeVar
from copy import copy
from dataclasses import dataclass
from flask import current_app as app
from dash import callback, Output, no_update as NOUPDATE
from dash_prefix import prefix
from dash_spa.logging import log
from dash_spa import callback
from dash_redux import ReduxStore



# Provides a React.Js context pattern that allows state to be easily passed
# between components
#
# See examples/react_pattern/pages/context_pattern.py

# TODO: Look at how to make this thread safe



# class State(dict):
#     """
#     Example:
#     m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])

#     https://stackoverflow.com/a/32107024/489239

#     """
#     def __init__(self, *args, **kwargs):
#         super(State, self).__init__(*args, **kwargs)
#         for arg in args:
#             if isinstance(arg, dict):
#                 for k, v in arg.items():
#                     self[k] = v

#         if kwargs:
#             for k, v in kwargs.items():
#                 self[k] = v

#     def __getattr__(self, attr):
#         return self.get(attr)

#     def __setattr__(self, key, value):
#         self.__setitem__(key, value)

#     def __setitem__(self, key, value):
#         super(State, self).__setitem__(key, value)
#         self.__dict__.update({key: value})

#     def __delattr__(self, item):
#         self.__delitem__(item)

#     def __delitem__(self, key):
#         super(State, self).__delitem__(key)
#         del self.__dict__[key]


# https://stackoverflow.com/a/32107024/489239
# https://stackoverflow.com/a/2352195/489239
# https://gist.github.com/golobor/397b5099d42da476a4e6

# class State():

#     def __init__(self, state, default = None):
#         for key, value in state.items():
#             self[key] = value

#         self._state = state
#         self._default = default

#     def __getattr__(self, name):
#         if name in self._state:
#             return self._state[name]
#         else:
#             return self._default

#     def __setattr__(self, name, value):
#         if name in ['_state', '_default']:
#             super().__setattr__(name, value)
#         else:
#             self._state[name] = value

#     def __getitem__(self, name):
#         return self.__getattr__(name)

#     def __setitem__(self, name, value):
#         self.__setattr__(name, value)


#     def update(self, dict):
#         self._state = dict.copy()

# https://docs.python.org/3/library/dataclasses.html


SelfContextState = TypeVar("SelfContextState", bound="ContextState")

@dataclass
class ContextState(dict):

    # def __setattr__(self, name, value):
    #     if name == 'search_term' and value is not None:
    #         log.info("ContextState name=%s = value=%s", name, value)
    #     super().__setattr__(name, value)

    def update(self, ref: str = None, state: SelfContextState = None) -> None:

        if ref is not None:
            if hasattr(self, ref):
                if state is not None:
                    setattr(self, ref, state)
                return

            raise AttributeError(f"Unknown attribute {ref}")

        for attr in state.__dict__.keys():
            if hasattr(self, attr):
                value = getattr(state, attr)
                if value is not None:
                    setattr(self, attr, value)
            else:
                raise AttributeError(f"Unknown attribute {ref}")

    def fromDict(self, state:dict):
         for attr in state.keys():
            if hasattr(self, attr):
                value = state[attr]
                setattr(self, attr, value)
            else:
                raise AttributeError(f"Unknown attribute {attr}")

    def toDict(self):
        return self.__dict__.copy()

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

            @callback(*_args, **_kwargs)
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

                # self._state.clear()
                prev_state = args.pop()
                self._state.fromDict(prev_state)

                self.contexts.set_context(self)

                # log.info('State[%s] state %s', self._store.id, self._state)

                user_func(*args)

                new_state = self._state.toDict()

                if prev_state == new_state:
                    new_state = NOUPDATE

                return new_state


        return wrapper

    def Provider(self, state:ContextState=None, id=id):

        assert id, "The context.Provider must have an id"

        self.id = id
        pid = prefix(id)

        # log.info('Provider id=%s', self.id)

        container_id = pid('container')

        # state can be provide when the context is created or passed in here

        self._state = copy(state) if state is not None else self._state
        self._store = ReduxStore(id=pid(), data=self._state.toDict(), storage_type='memory')

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

                result.children.append(self._store)

                return result

            self.render = func_wrapper

            return func_wrapper

        # Render the container if the context store has been modified

        @callback(Output(container_id, 'children'), self._store.input.data, prevent_initial_call=True)
        def container_cb(state):
            log.info('Update container %s, %s', container_id, state)

            # self._state.clear()
            self._state.fromDict(state)
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
        state = self._state[ref] if ref else self._state
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
