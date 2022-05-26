from dash import html, no_update as NOUPDATE
from dash import html, callback, Output
import dash_holoniq_components as dhc
from dash_spa import prefix, register_page, page_container_append
from dash_spa.logging import log

from dash_redux import ReduxStore

register_page(__name__, path='/', title="Button Test", short_name='Buttons')

pfx = prefix("redux_test")

def page_layout():

    store = ReduxStore(id=pfx('store'), data={})
    btn1 = html.Button("Button1", id=pfx('btn1'))
    btn2 = html.Button("Button2", id=pfx("btn2"))
    container = html.Div(id=pfx('container'))

    @store.update(btn1.input.n_clicks)
    def btn1_update(clicks, store):
        if clicks:
            log.info('Btn 1 clicked %d', clicks)
            if 'btn1' in store:
                store['btn1'] += 1
            else:
                store['btn1'] = 1
        return store


    @store.update(btn2.input.n_clicks)
    def btn2_update(clicks, store):
        if clicks:
            log.info('Btn 2 clicked %d', clicks)
            if 'btn2' in store:
                store['btn2'] += 1
            else:
                store['btn2'] = 1
        return store


    @callback(container.output.children, store.store.input.data)
    def btn2_update(store):
        msg = ""
        if store and 'btn1' in store:
            msg += f"Button 1 pressed {store['btn1']} times "

        if store and 'btn2' in store:
            msg += f"Button 2 pressed {store['btn2']} times "

        return msg

    return html.Div([btn1, btn2, container, store])


layout = page_layout()
