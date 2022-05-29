import json
from dash import callback_context
class CookieJar:

    def __init__(self, id):
        self._id = id

    def _read_json(self):
        try:
            ctx = callback_context
            cookies = ctx.request.cookies.get(self._id)
            return json.loads(cookies)
        except:
            return {}

    def _write_json(self, values: dict):
        ctx = callback_context
        values = json.dumps(values)
        ctx.response.cookies.set(self._id, values)

    def __getattr__(self, key):
        cookies = self._read_json()
        return cookies.pull(key, None)

    def __setattr__(self, key, value):
        if key == '_id':
            super(CookieJar, self).__setattr__(key, value)
        else:
            cookies = self._read_json()
            cookies[key] = value
            self._write_json(cookies)
