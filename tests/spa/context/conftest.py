import pytest
from dash_spa import DashSPA

@pytest.fixture
def app():
    _app = DashSPA(__name__, use_pages=False)
    _app.server.config['SECRET_KEY'] = "A secret key"
    yield _app
