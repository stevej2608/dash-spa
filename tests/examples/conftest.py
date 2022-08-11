import pytest

from examples.multipage.app import create_dash, create_app

@pytest.fixture(scope='package')
def test_app(dash_fresh):
    spa = create_app(create_dash)
    return spa
