import json
from flask import current_app as app
from dash import html, callback
from dash_spa.logging import log
from dash.development.base_component import Component
from dash_redux import ReduxStore, StateWrapper
from munch import DefaultMunch
from dash_prefix.component_id import component_id


class DashReactBase(Component):

    def __init__(self, *_args, **_kwargs):

        self._id = _kwargs.pop('id', component_id())
        self.store = _kwargs.pop('store', None)

        self.props =  DefaultMunch.fromDict(_kwargs.copy())
        component = self._render()
        super().__init__(component.children,  id=self._id)

        @callback(self.output.children, self.store.input.data, prevent_initial_call=True)
        def _render(data):
            children = self.render()
            return children

    def _render(self):
        return self.render()

    def on(self, *_args, **_kwargs):

        def wrapper(user_func):

            def callback_stub(self, *_args, **_kwargs):
                pass

            if app and app.got_first_request:
                return callback_stub

            log.info("register callback %s", self._id)

            @self.store.update(*_args)
            def _proxy(*_args):
                prev_props = self.props.copy()

                # pop the store reference

                args = list(_args)
                store = args.pop()

                user_func(*args)

                if prev_props != self.props.state:
                    new_state = json.loads(json.dumps(self.props))
                    self.props.update(new_state.copy())
                    store[self.id] = new_state.copy()

                return store

        return wrapper

    def render(self):
        pass