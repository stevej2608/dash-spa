import json
from typing import Any

from _plotly_utils.utils import PlotlyJSONEncoder
from dash_spa.spa_config import config
from .session_backend import SessionBackend

options = config.get('session_storage.redis')

# https://github.com/T4rk1n
# https://github.com/plotly/dash-labs/blob/sessions/dash_labs/session/__init__.py

class RedisSessionBackend(SessionBackend):
    """
    Session backend using redis.
    """

    def __init__(self, session_id):
        self.session_id = session_id

        port = options.port or 6379
        host = options.host or 'localhost'
        db = options.db or 0

        expire = options.expire or None

        connection_kwargs = {}

        try:
            import redis
        except ImportError as err:
            raise ImportError(
                "Diskcache is not installed, install it with "
                "`pip install redis`"
            ) from err

        self.pool = redis.ConnectionPool(host=host, port=port, db=db, **connection_kwargs)
        self.r = redis.Redis(connection_pool=self.pool)
        self.expire = expire

    def _session_key(self):
        return f"dash_spa/session/{self.session_id}"

    def get(self, obj_key: str):
        value = self.r.hget(self._session_key(), obj_key)
        if value:
            return json.loads(value)
        else:
            return {}

    def set(self, obj_key: str, value: Any):
        self.r.hset(self._session_key(), obj_key, json.dumps(value, cls=PlotlyJSONEncoder))
        if self.expire:
            self.r.expire(self._session_key(), self.expire)

