import pytest

from app import create_dash
from examples.multipage import create_spa

@pytest.fixture(scope='package')
def spa():
    """An SPA Application for the admin tests."""
    dash = create_dash()
    spa = create_spa(dash)
    return spa
