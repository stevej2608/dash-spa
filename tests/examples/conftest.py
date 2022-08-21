import pytest
from examples.multipage.app import create_dash, create_app

@pytest.fixture
def test_app():
    spa = create_app(create_dash)
    yield spa
