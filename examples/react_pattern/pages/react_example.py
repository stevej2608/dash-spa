import json
from flask import current_app as app
from dash import html
from dash import html, callback
from dash_spa import prefix, register_page, NOUPDATE
from dash_spa.logging import log
from dash_spa.components.local_storage import LocalStore
from dash.development.base_component import Component
from dash_redux import ReduxStore, StateWrapper
from munch import DefaultMunch
from dash_prefix.component_id import component_id


register_page(__name__, path='/', title="React Pattern", short_name='React')

pfx = prefix("storage_test")


class DashReactBase(Component):

    IDS = {}

    def __init__(self, *_args, **_kwargs):

        if not 'id' in _kwargs:
            _kwargs['id'] = component_id()

        self.id = _kwargs['id']

        self.store = _kwargs.pop('store', None)
        self.props =  DefaultMunch(None,_kwargs.copy())
        component = self._render()
        super().__init__(component.children,  id=_kwargs['id'])


    def instance_id(self):
        class_name = self.__class__.__name__
        if not class_name in DashReactBase.IDS:
            DashReactBase.IDS[class_name] = 0
        DashReactBase.IDS[class_name] += 1
        return f"{class_name}_{DashReactBase.IDS[class_name]}"

    def _render(self):
        return self.render()

    def on(self, *_args, **_kwargs):

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

                if prev_props != self.props.state:
                    children = self.render()
                    self.children = children
                    new_state = json.loads(json.dumps(self.props))
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
        gid = self.props.id
        pfx = prefix(gid)

        title = html.H4(f"Button {gid}")
        btn1 = html.Button("Button1", id=pfx('btn1'))
        btn2 = html.Button("Button2", id=pfx("btn2"))
        container = html.Div(f"Button Group {gid}", id=pfx('container'))

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

    store = ReduxStore(id='test_store', data={})

    group1 = ButtonGroup(id='group_1', store=store)
    group2 = ButtonGroup(id='group_2', store=store)

    store_view = html.Div(id='store_view')

    @callback(store_view.output.children, store.input.data)
    def view_cb(store):
        groups = [html.H4(f"{key} {item}") for key, item in store.items()]
        return groups

    return html.Div([store, group1, group2, store_view])


layout = page_layout()
