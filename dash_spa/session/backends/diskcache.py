import appdirs
import json
from dash_spa.logging import log
from dash_spa.spa_config import config
from dash_spa.utils.json_coder import json_decode, json_encode

from .session_backend import SessionBackend

options = config.get('session_storage')

_cache_dir = options.diskcache_folder or appdirs.user_cache_dir("dash_spa-sessions")

class SessionDiskCache(SessionBackend):
    """Wrapper for an individual session

    A single json string, indexed on session_id, is held in
    the server-side session cache. The cache should be thread and
    multi-process safe since each session has a uniq id and all the
    session data is stored on a single key.

    Use get(key) to get the value of an individual element in session dict.

    Use update() to save the entire session data dict

    Use clear() to remove all session entries from the cache

    """

    # TODO: Figure out how to test if this is thread & process safe

    try:
        # pylint: disable=import-outside-toplevel
        from diskcache import Cache
    except ImportError as err:
        raise ImportError(
            "Diskcache is not installed, install it with "
            "`pip install diskcache`"
        ) from err


    _disk_cache =  Cache(directory = f"{options.folder or _cache_dir}")

    expiry = options.get('expire_days', 30) * 24 * 60 * 60

    def __init__(self, session_id):
        self.session_id = session_id

        if self.session_id in SessionDiskCache._disk_cache:
            json_str = SessionDiskCache._disk_cache[self.session_id]
            self.session_store = json.loads(json_str, object_hook=json_decode)
        else:
            log.info("Create new session store id=%s", self.session_id)
            self.session_store = {}

    def _update(self):
        """Write the session state to the store"""

        # log.info('write cache[%s]=%s', self.session_id, self.session_store)
        json_str = json.dumps(self.session_store, default=json_encode)
        SessionDiskCache._disk_cache.set(self.session_id, json_str, self.expiry)


    def get(self, obj_key) -> dict:
        """Get current session value for the given key"""
        if not obj_key in self.session_store:
            self.session_store[obj_key] = {}
        return self.session_store[obj_key]


    def set(self, obj_key, value: dict):
        """Save the session value against the given key and update the session store if needed"""

        # previous value

        prev_state = json.dumps(self.get(obj_key), sort_keys = True)

        # Save new value

        self.session_store[obj_key] = value

        # Update if changed

        new_state = json.dumps(self.get(obj_key), sort_keys = True)
        if new_state != prev_state:
            self._update()

    def remove(self, obj_key):
        """ Remove given key and update the store"""
        self.session_store.pop(obj_key, None)
        self._update()

    @staticmethod
    def clear():
        """Remove all items from cache.

        Removing items is an iterative process. In each iteration, a subset of
        items is removed. Concurrent writes may occur between iterations.
        """
        SessionDiskCache._disk_cache.clear()
