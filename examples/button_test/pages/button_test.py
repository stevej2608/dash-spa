from dash import html
from dash_spa import prefix, register_page, callback, NOUPDATE

from dash_redux import ReduxStore

register_page(__name__, path='/', title="Button Test", short_name='Buttons')

# Example demonstrates basic use of ReduxStore to manage several instances
# of a button_toolbar(). Button clicks update the redux store. The toolbar
# state is reported locally within toolbar UI. In addition the the last
# button clicked in any of the toolbars is reported.
#
# Since the ReduxStore default storage type is "session" the button state
# is persistent. This would make a useful pattern for a shopping trolley.
#
# See examples/context/pages/context_pattern.py for a far better
# generic toolbar supporting any number of buttons

pfx = prefix("redux_test")

store = ReduxStore(id=pfx('store'), data={})

def button_toolbar(toolbar_title: str):
    pfx = prefix(toolbar_title)

    def store_ref(title, store):
        if not title in store:
            store[title] = {'btn1': 0, 'btn2': 0}
        return store[title]

    title = html.H4(f"Button {toolbar_title}")
    btn1 = html.Button("Button1", id=pfx('btn1'))
    btn2 = html.Button("Button2", id=pfx("btn2"))
    container = html.Div("", id=pfx('container'))

    @store.update(btn1.input.n_clicks)
    def btn1_update(clicks, store):
        tb_store = store_ref(toolbar_title, store)
        if clicks:
            tb_store['btn1'] += 1
            store['last'] = f"{toolbar_title}.btn1(clicks={tb_store['btn1']})"

        return store

    @store.update(btn2.input.n_clicks)
    def btn2_update(clicks, store):
        tb_store = store_ref(toolbar_title, store)
        if clicks:
            tb_store['btn2'] += 1
            store['last'] = f"{toolbar_title}.btn2(clicks={tb_store['btn2']})"
        return store

    # Report toolbar state locally

    @callback(container.output.children, store.input.data)
    def btn_message(store):
        tb_store = store_ref(toolbar_title, store)
        msg = f"btn1 {tb_store['btn1']} clicks, btn2 {tb_store['btn2']} clicks"
        return msg

    return html.Div([title, btn1, btn2, container, html.Br()])

def layout():

    tb1 = button_toolbar('Toolbar1')
    tb2 = button_toolbar('Toolbar2')
    tb3 = button_toolbar('Toolbar3')

    # Report last button clicked

    report = html.H3("", id=pfx('report'))

    @callback(report.output.children, store.input.data)
    def cb_update(store):
        if 'last' in store:
            return f"Button {store['last']} clicked last"
        else:
            return NOUPDATE

    # Return page layout

    return html.Div([store, tb1, tb2, tb3, report])
