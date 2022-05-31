import json
from flask import current_app as app
from dash import html, Output
from dash import html, callback
from dash_spa import prefix, register_page, NOUPDATE
from dash_spa.logging import log
from dash_spa.components.local_storage import LocalStore
from dash.development.base_component import Component
from dash_redux import ReduxStore, StateWrapper
from munch import DefaultMunch
from dash_prefix.component_id import component_id


register_page(__name__, path='/', title="React Pattern", short_name='React')

pfx = prefix("storage_test2")


class DashReactBase(Component):

    # IDS = {}

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
                    self.props =  DefaultMunch.fromDict(new_state.copy())
                    store[self.id] = new_state

                return store

        return wrapper

    def render(self):
        pass

    def set_props(self, props):
        # log.info('set_props %s : %s', self.id, props)
        self.props = DefaultMunch(None, props)


class ButtonGroup(DashReactBase, html.Div):

    def render(self):
        # log.info("render %s props = %s", self.id, self.props)
        gid = self._id
        pfx = prefix(gid)

        title = html.H4(f"Button {gid}")
        btn1 = html.Button("Button1", id=pfx('btn1'))
        btn2 = html.Button("Button2", id=pfx("btn2"))

        props = self.props

        msg = ""
        if 'btn1' in props:
            msg += f"Button 1 pressed {props.btn1} times "

        if 'btn2' in props:
            msg += f"Button 2 pressed {props.btn2} times "

        container = html.Div(msg)

        @self.on(btn1.input.n_clicks)
        def btn1_update(clicks):
            if clicks:
                props = self.props
                if 'btn1' in props:
                    props.btn1 += 1
                else:
                    props.btn1 = 1
                self.set_props(props)


        @self.on(btn2.input.n_clicks)
        def btn2_update(clicks):
            if clicks:
                props = self.props
                if 'btn2' in props:
                    props.btn2 += 1
                else:
                    props.btn2 = 1
                self.set_props(props)


        return html.Div([title, btn1, btn2, container, html.Br()])


def page_layout():

    store = ReduxStore(id='test_store_1', data={})

    group1 = ButtonGroup(id='group_1', store=store)
    group2 = ButtonGroup(id='group_2', store=store)

    store_view = html.Div(id='store_view')

    @callback(store_view.output.children, store.input.data)
    def view_cb(store):
        groups = [html.H4(f"{key} {item}") for key, item in store.items()]
        return groups

    return html.Div([store, group1, group2, store_view])


layout = page_layout()
