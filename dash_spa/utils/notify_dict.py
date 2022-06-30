# https://stackoverflow.com/a/5186698/489239

class NotifyDict(dict):
    __slots__ = ["callback"]

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        dict.__init__(self, *args, **kwargs)


    def _wrap(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self.callback()
            return result
        return wrapper


    __delitem__ = _wrap(dict.__delitem__)
    __setitem__ = _wrap(dict.__setitem__)
    clear = _wrap(dict.clear)
    pop = _wrap(dict.pop)
    popitem = _wrap(dict.popitem)
    setdefault = _wrap(dict.setdefault)
    update =  _wrap(dict.update)