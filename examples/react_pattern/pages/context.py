import json
from flask import current_app as app
from dash import html, no_update as NOUPDATE
from dash import html, callback, Output
import dash_holoniq_components as dhc
from dash_spa import prefix, register_page, page_container_append
from dash_spa.logging import log
from dash.development.base_component import Component
from dash_redux import ReduxStore
from munch import DefaultMunch
from dash_prefix import copy_factory

# https://www.digitalocean.com/community/tutorials/how-to-share-state-across-react-components-with-context

class _ContextWrapper:

    @property
    def input(self):
        return self.store.input

    @property
    def output(self):
        return self.store.output

    @property
    def state(self):
        return self.store.state

    def __init__(self, **kwargs):
        self.id = kwargs.pop('_id')
        self.props = kwargs.copy()


    def On(self, *_args, **_kwargs):

        def wrapper(user_func):

            def callback_stub(self, *_args, **_kwargs):
                pass

            if app and app.got_first_request:
                return callback_stub

            log.info("register callback %s", self.id)

            @self.store.update(*_args)
            def _proxy(*_args):
                prev_props = self.props.copy()

                # pop the store reference

                args = list(_args)
                store = args.pop()

                result = user_func(*args)

                if prev_props != self.props:
                    children = self.render().children

                    for idx in range(len(children)):
                        self.children[idx] = children[idx]

                    new_state = self.props.copy()
                    self.props = DefaultMunch.fromDict(new_state)
                    store = new_state

                return store

        return wrapper

    def Provider(self, props=None):

        self.props = DefaultMunch.fromDict(props.copy() if props is not None else self.props)
        self.store = ReduxStore(id=self.id, data=self.props)

        def provider_decorator(func):

            def func_wrapper( *_args, **_kwargs):
                result = func(*_args, **_kwargs)


                if not isinstance(result.children, list):
                    result.children = [result.children]

                result.children.append(self.store)

                if not hasattr(self, 'children'):
                    self.children = result.children

                return result

            self.render = func_wrapper

            return func_wrapper
        return provider_decorator


def createContext(props={}, id=None):
    return _ContextWrapper(**props, _id=id)

def useContext(ctx: _ContextWrapper):
    return ctx
