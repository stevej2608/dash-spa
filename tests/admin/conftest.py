import pytest

from dash_spa.spa_pages import clear_globals
from usage import create_dash, create_app

@pytest.fixture(scope='function')
def test_app():
    """An SPA Application for the admin tests."""
    spa = create_app(create_dash)
    yield spa
    # clear_globals()
