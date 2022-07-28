from functools import wraps

def synchronized(lock):
    @wraps
    def _wrapper(wrapped, args, kwargs):
        with lock:
            return wrapped(*args, **kwargs)
    return _wrapper
