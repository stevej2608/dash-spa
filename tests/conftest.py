import logging
import pytest

from app import app as dash_app
from selenium.webdriver.chrome.options import Options
from usage import create_spa

# Turn off werkzeug logging as it's very noisy

aps_log = logging.getLogger('werkzeug')
aps_log.setLevel(logging.ERROR)


# This is needed to force Chrome to run without sandbox enabled. Docker
# does not support namespaces so running Chrome in a sandbox is not possible.
#
# See https://github.com/plotly/dash/issues/1420

def pytest_setup_options():
    options = Options()
    options.add_argument('--no-sandbox')
    # options.add_argument("--start-maximized")
    return options


@pytest.fixture(scope='package')
def app(spa):
    return spa.dash.server

@pytest.fixture(scope='package')
def client(app):
    """A client for the Flask tests."""
    _client = app.test_client()
    yield _client

@pytest.fixture(scope='function')
def duo(dash_duo, spa):
    """A client for the dash_duo/Flask tests."""
    dash_duo.start_server(spa.dash)

    dash_duo.driver.set_window_size(1500, 1100)
    dash_duo.driver.maximize_window()

    return dash_duo
