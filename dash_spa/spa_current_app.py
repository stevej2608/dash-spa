from werkzeug.local import LocalProxy
from dash import get_app
from .spa_pages import DashSPA

def _get_current_app() -> DashSPA:
    try:
        return get_app()
    except Exception:
        pass
    return None

current_app = LocalProxy(_get_current_app)