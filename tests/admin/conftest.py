import pytest

from usage import create_dash, create_app


@pytest.fixture
def test_app():
    """An SPA Application for the admin tests."""
    spa = create_app(create_dash)
    yield spa



