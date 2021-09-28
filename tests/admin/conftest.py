import pytest

from app import app as dash_app

from usage import create_spa

@pytest.fixture(scope='package')
def spa():
    """An SPA Application for the admin tests."""
    spa = create_spa(dash_app)
    return spa
