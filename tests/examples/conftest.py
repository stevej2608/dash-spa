import pytest
from dash_spa.spa_globals import Globals
from examples.multipage.app import create_dash, create_app

@pytest.fixture
def test_app():
    Globals.clear()
    spa = create_app(create_dash)
    yield spa
    Globals.clear()
