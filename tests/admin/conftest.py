import pytest

from usage import create_dash, create_app

@pytest.fixture(scope='function')
def test_app():
    """An SPA Application for the admin tests."""
    spa = create_app(create_dash)
    return spa
