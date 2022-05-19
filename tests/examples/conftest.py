import pytest

from examples.multipage.app import create_dash, create_app

# https://pypi.org/project/pytest-pyppeteer/


@pytest.fixture(scope='package')
def spa():
    spa = create_app(create_dash)
    return spa
