from urllib.parse import urlparse
from dash_spa import page_container_append, location, callback, NOUPDATE
from dash_spa.logging import log
from dash_redux import ReduxStore

store = ReduxStore(id='location_store', data=None, storage_type='memory')

page_container_append(store)

@callback(location.output.href, location.state.href, store.input.data, prevent_initial_callback=True)
def _location_update(url, data):
    log.info('location update %s', data)
    parts = urlparse(url)
    if data and data != parts.path:
        return data
    else:
        return NOUPDATE
