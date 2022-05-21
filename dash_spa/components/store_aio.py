from dash import html, dcc
from dash_spa import prefix, page_container_append

class StoreAIO:

    container = html.Div([], id='_aio_storage')

    page_container_append(container)

    @staticmethod
    def create_store(data: dict={}, id=None):
        pid = prefix(id)
        store = dcc.Store(id=pid(), data=data)
        StoreAIO.container.children.append(store)
        return store

    @staticmethod
    def Location(id=None):
        pid = prefix(id)
        loc = dcc.Location(id=pid())
        StoreAIO.container.children.append(loc)
        return loc

