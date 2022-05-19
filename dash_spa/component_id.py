import threading

_THREAD_LOCK = threading.Lock()
_GLOBAL_ID = 0x0ffff

def component_id() ->str:
    global _GLOBAL_ID
    with _THREAD_LOCK:
        _GLOBAL_ID += 1
    return f'i{hex(_GLOBAL_ID)[2:]}'
