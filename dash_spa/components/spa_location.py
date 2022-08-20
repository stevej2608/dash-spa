from flask import current_app as app
from werkzeug.local import LocalProxy
from urllib.parse import urlparse
from dash._callback import GLOBAL_CALLBACK_MAP
from dash_spa import page_container_append, callback, NOUPDATE, current_app
from dash_spa.logging import log
from dash_redux import ReduxStore
import dash_holoniq_components as dhc

# Use ReduxStore many-to-one capability to allow any event in any page to
# update the browser location. Use SPA_LOCATION.update callback:
#
# from dash_spa import SPA_LOCATION
#
# @SPA_LOCATION.update(ticker_dropdown.input.value)
# def _update_loc(value, store):
#     ...
#     return { 'href': href }
#
# See pages/ticker.py for working example

class LocationStore(ReduxStore):

    def update(self, *_args, **_kwargs):

        def callback_stub(self, *_args, **_kwargs):
            pass

        if app and app.got_first_request:
            return callback_stub

        return super().update(*_args, **_kwargs)


def _create_location():

    if not current_app:
        return None

    if 'spa_location_store.data' not in GLOBAL_CALLBACK_MAP:
        _create_location.singleton = LocationStore(id='spa_location_store', data=None, storage_type='session')

        _location = dhc.Location(id='spa_location', refresh=False)

        @callback(_location.output.href, _location.state.href, _create_location.singleton.input.data, prevent_initial_call=True)
        def _location_update(url, data):
            if data and 'href' in data:
                url = urlparse(url)
                href = data['href']
                new_url = urlparse(href)
                if url.path != new_url.path or url.query != new_url.query:
                    # log.info('location update, href=%s', href)
                    return href

            return NOUPDATE

        page_container_append(_location)
        page_container_append(_create_location.singleton)

    return _create_location.singleton


SPA_LOCATION = LocalProxy(_create_location)
