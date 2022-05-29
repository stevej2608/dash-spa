from dash import html
from dash import html, callback
from dash_spa import prefix, register_page, NOUPDATE
from dash_spa.logging import log
from dash_spa.components.local_storage import LocalStore


register_page(__name__, path='/', title="Storage Test", short_name='Storage')

pfx = prefix("storage_test")


local_store = LocalStore(id=pfx())


def button_group(gid):
    pfx = prefix(gid)

    title = html.H4(f"Button {gid}")
    btn1 = html.Button("Button1", id=pfx('btn1'))
    btn2 = html.Button("Button2", id=pfx("btn2"))
    container = html.Div(f"Button Group {gid}", id=pfx('container'))

    def get_section(store, section):
        if not section in store:
            store[section] = {}
        return store[section]

    @local_store.update(btn1.input.n_clicks, prevent_initial_callback=True)
    def btn1_update(clicks, store):
        if clicks:
            section = get_section(store, gid)
            log.info('Btn%s 1 clicked %d', gid, clicks)
            if 'btn1' in section:
                section['btn1'] += 1
            else:
                section['btn1'] = 1
        return store


    @local_store.update(btn2.input.n_clicks, prevent_initial_callback=True)
    def btn2_update(clicks, store):
        if clicks:
            section = get_section(store, gid)
            log.info('Btn%s 2 clicked %d', gid, clicks)
            if 'btn2' in section:
                section['btn2'] += 1
            else:
                section['btn2'] = 1
        return store


    @callback(container.output.children, local_store.input.data)
    def container_update(store):
        section = get_section(store, gid)
        log.info('container_update%s update %s', gid, section)
        msg = ""
        if 'btn1' in section:
            msg += f"Button 1 pressed {section['btn1']} times "

        if 'btn2' in section:
            msg += f"Button 2 pressed {section['btn2']} times "

        return msg

    return html.Div([title, btn1, btn2, container, html.Br()])



def page_layout():

    group1 = button_group('group_1')
    group2 = button_group('group_2')

    store_view = html.Div(id='store_view')

    @callback(store_view.output.children, local_store.input.data)
    def view_cb(store):
        groups = [html.H4(f"{key} {item}") for key, item in store.items()]
        return groups

    return html.Div([group1, group2, store_view])


layout = page_layout()
