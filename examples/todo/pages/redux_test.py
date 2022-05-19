from dash import html, no_update as NOUPDATE
from dash import html, callback

from dash_spa import prefix, register_page, page_container_append
from dash_spa.logging import log

from dash_spa.components.redux_store import ReduxStore

register_page(__name__, path='/redux_test', title="Dash Todo", short_name='Todo')

pfx = prefix("redux_test")

Redux = ReduxStore(id=pfx('store'), storage_type='session',
        data = {
            "btn1" : 0,
            "btn2" : 0,
            }
        )

def page_layout():
    btn1 = html.Button("Button 1", id=pfx('btn1'))
    btn2 = html.Button("Button 2", id=pfx('btn2'))
    container = html.Div(id=pfx('container'))

    @Redux.update(btn1.input.n_clicks)
    def btn1_update(clicks, store):
        if clicks:
            log.info('Btn 1 clicked %d (%s)', clicks, store)
            store['btn1'] += 1
            return store
        return NOUPDATE

    @Redux.update(btn2.input.n_clicks)
    def btn2_update(clicks, store):
        if clicks:
            log.info('Btn 2 clicked %d (%s)', clicks, store)
            store['btn2'] += 1
            return store
        return NOUPDATE

    @callback(container.output.children, Redux.store.input.data)
    def container_update(store):
        if store:
            return f"Btn 1 clicked {store['btn1']} times, Btn 2 clicked {store['btn2']} times"
        return NOUPDATE

    return html.Div([btn1, btn2, container])

page_container_append(Redux)

layout = page_layout()
