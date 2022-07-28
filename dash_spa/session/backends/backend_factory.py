import flask
from dash_spa.spa_config import config, ConfigurationError

from .diskcache import SessionDiskCache
from .redis import RedisSessionBackend
from .postgres import PostgresSessionBackend

from ..session_cookie import session_manager

options = config.get('session_storage')

class SessionBackendFactory:

    user_sessions = {}

    @staticmethod
    def get_cache():

        session_id = session_manager.get_session_id()

        def create_session(session_id):
            cache_type = options.get('backend', 'diskcache')

            if cache_type == 'diskcache': return SessionDiskCache(session_id)
            if cache_type == 'redis': return RedisSessionBackend(session_id)
            if cache_type == 'postgres': return PostgresSessionBackend(session_id)

            raise ConfigurationError(f"Unsupported backend {cache_type}")

        if not session_id in SessionBackendFactory.user_sessions:
            SessionBackendFactory.user_sessions[session_id] = create_session(session_id)

        return SessionBackendFactory.user_sessions[session_id]


