import pytest

from dash_spa.spa_globals import Globals

from usage import create_dash, create_app


@pytest.fixture
def test_app():
    """An SPA Application for the admin tests."""

    # Globals.restore()

    spa = create_app(create_dash)
    yield spa

    # Globals.save()
    Globals.clear()


