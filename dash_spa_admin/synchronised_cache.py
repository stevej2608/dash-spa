from functools import wraps
import threading
from cachetools import TTLCache
import time


def synchronized(lock):
    @wraps
    def _wrapper(wrapped, args, kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrapper

class SynchronisedTTLCache:

    # https://rszalski.github.io/magicmethods/

    def __init__(self, maxsize, ttl, timer=time.monotonic, getsizeof=None):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl, timer=timer, getsizeof=getsizeof)
        self._lock = threading.Lock()

    def __len__(self):
        @synchronized(self._lock)
        def inner():
            return self._cache.__len__
        return inner()

    def __getitem__(self, key):
        @synchronized(self._lock)
        def inner():
            return self._cache.__getitem__(key)
        return inner()

    def __setitem__(self, key, value):
        @synchronized(self._lock)
        def inner():
            return self._cache.__setitem__(key, value)
        return inner()

    def __delitem__(self, key):
        @synchronized(self._lock)
        def inner():
            return self._cache.__delitem__(key)
        return inner()

    def keys(self):
        @synchronized(self._lock)
        def inner():
            return self._cache.keys()
        return inner()

    def __iter__(self):
        @synchronized(self._lock)
        def inner():
            return self._cache.__iter__()
        return inner()

    def __reversed__(self):
        @synchronized(self._lock)
        def inner():
            return self._cache.__reversed__()
        return inner()
