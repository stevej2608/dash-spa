import pytest

@pytest.fixture(scope='package')
def test_app():
    from examples.multipage.app import app, create_app
    spa = create_app(app)
    yield spa
    #clear_globals()

