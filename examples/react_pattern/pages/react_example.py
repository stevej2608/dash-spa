import json
from dash import html
from dash import html, callback
from dash_spa import prefix, register_page

from dash_redux import ReduxStore

from .react_base import DashReactBase


register_page(__name__, path='/', title="React Pattern", short_name='React')

pfx = prefix("storage_test")

class ButtonGroup(DashReactBase, html.Div):

    def render(self):
        # log.info("render %s props = %s", self.id, self.props)
        gid = self._id
        pfx = prefix(gid)

        title = html.H4(f"Button {gid}")
        btn1 = html.Button("Button1", id=pfx('btn1'))
        btn2 = html.Button("Button2", id=pfx("btn2"))

        props = self.props

        msg = f"Button 1 pressed {props.btn1} times, Button 2 pressed {props.btn2} times "

        container = html.Div(msg)

        @self.on(btn1.input.n_clicks)
        def btn1_update(clicks):
            if clicks:
                if 'btn1' in props:
                    props.btn1 += 1
                else:
                    props.btn1 = 1


        @self.on(btn2.input.n_clicks)
        def btn2_update(clicks):
            if clicks:
                if 'btn2' in props:
                    props.btn2 += 1
                else:
                    props.btn2 = 1


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
