from urllib.parse import urlparse
from dash_spa import page_container_append, callback, NOUPDATE
from dash_spa.logging import log
from dash_redux import ReduxStore
import dash_holoniq_components as dhc

SPA_LOCATION = ReduxStore(id='spa_location_store', data=None, storage_type='session')

page_container_append(SPA_LOCATION)

location = dhc.Location(id='spa_location', refresh=False)
page_container_append(location)

@callback(location.output.href, location.state.href, SPA_LOCATION.input.data, prevent_initial_call=True)
def _location_update(url, data):
    if data and 'href' in data:
        url = urlparse(url)
        href = data['href']
        new_url = urlparse(href)
        if url.path != new_url.path or url.query != new_url.query:
            log.info('location update, href=%s', href)
            return href

    return NOUPDATE
