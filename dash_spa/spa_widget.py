from dash_prefix import prefix
from .utils.caller import caller_hash
from .logging import log

class SPAWidget:

    def __init__(self):
        self._prefix = None

    def prefix(self):
        if not hasattr(self, '_prefix')  or self._prefix is None:
            self._prefix = prefix(caller_hash(2, "wgt_"))
        return self._prefix
