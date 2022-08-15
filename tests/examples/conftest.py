import pytest

from dash_spa.spa_pages import clear_globals
from examples.multipage.app import app, create_app

@pytest.fixture(scope='package')
def test_app():
    spa = create_app(app)
    yield spa
    #clear_globals()

