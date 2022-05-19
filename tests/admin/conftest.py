import pytest

from usage import create_dash, create_app

@pytest.fixture(scope='function')
def spa():
    """An SPA Application for the admin tests."""
    spa = create_app(create_dash)
    return spa
