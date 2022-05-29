import time
from flask import session
from dash import callback, html
from dash_spa import page_container_append, NOUPDATE
from dash_spa.logging import log

from ..spa_current_user import current_user
from dash_spa_admin.synchronised_cache import SynchronisedTTLCache

from dash_redux import ReduxStore

LAST_MODIFIED = '_last_modified'

# TODO: App config using local store, is this a good idea?  Need to look at using server
# database.


class LocalStore(ReduxStore):

    def __init__(self, id, storage_type='local'):
        super().__init__(id=id, data={}, storage_type=storage_type)
        self.cache = SynchronisedTTLCache(1000,ttl=SynchronisedTTLCache.FOREVER)

        log.info('CREATE LOCAL STORE')

        @callback(self.output.clear_data, self.input.data)
        def _startup_cb(data):

            for user in data.keys():
                log.info('Stored config for %s = %s', user, data[user])
                self.cache[user] = data[user].copy()
            return NOUPDATE

        page_container_append(self)

    def get_config(self, id):
        user = current_user.name.lower()
        if not user in self.cache:
            return None

        if id in self.cache[user]:
            return self.cache[user][id]
        else:
            return None

    @staticmethod
    def get_user(id, store):
        user = current_user.name.lower()

        if not user in store:
            store[user] = {}

        if id in store[user]:
            return store[user][id]
        else:
            return None

    @staticmethod
    def set_user(id, store, segment):
        user = current_user.name.lower()

        if user not in store:
            store[user] = {}

        if store[user][id] != segment:
            log.info('Updating %s.%s', user, id)
            store[user][id] = segment
            store[user][LAST_MODIFIED] = int((time.time() + 0.5) * 1000)
            return store

        log.info('%s.%s - NOUPDATE', user, id)

        return NOUPDATE


    #     self.callers = []

    #     @callback(self.output.data, self.input.data)
    #     def _update_store(store):
    #         user = current_user.name

    #         if user in store:
    #             user_store = store[user].copy()
    #         else:
    #             user_store = {}

    #         for caller in self.callers:
    #             result = caller(user_store)
    #             if result != NOUPDATE and result != None:
    #                 user_store.update(result)

    #         store[user] = user_store
    #         return store

    #     super().__init__(id=id, storage_type='local')

    # def register_callback(self, callback):
    #     self.callers.append(callback)


class SessionStore(ReduxStore):

    def __init__(self, id, storage_type='session'):
        super().__init__(id=id, data={}, storage_type=storage_type)
        self.cache = SynchronisedTTLCache(1000,ttl=SynchronisedTTLCache.FOREVER)

        log.info('CREATE SESSION STORE')

        @self.update(self.input.modified_timestamp)
        def _session_cb(timestamp, data):
            log.info(f'NEW BROWSER TAB %s, %s', data, timestamp)
            session['ID'] = timestamp

            if data:
                return NOUPDATE
            else:
                return {'ID' : timestamp }

        page_container_append(self)
