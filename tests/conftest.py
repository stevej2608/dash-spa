import logging
import pytest
from selenium.webdriver.chrome.options import Options

from dash._callback import GLOBAL_CALLBACK_MAP, GLOBAL_CALLBACK_LIST

# Turn off werkzeug logging as it's very noisy

aps_log = logging.getLogger('werkzeug')
aps_log.setLevel(logging.ERROR)


# https://dash.plotly.com/testing

def pytest_setup_options():
    options = Options()
    options.add_argument('--disable-gpu')
    # options.add_argument("user-data-dir=tmp/pytest/custom/profile")

    # This is needed to force Chrome to run without sandbox enabled. Docker
    # does not support namespaces so running Chrome in a sandbox is not possible.
    #
    # See https://github.com/plotly/dash/issues/1420

    options.add_argument('--no-sandbox')

    return options

# https://flask.palletsprojects.com/en/1.1.x/api/#flask.testing.FlaskClient
# https://stackoverflow.com/a/62379417/489239

@pytest.fixture(scope='function')
def test_client(test_app):
    """A client for the Flask tests."""
    _client = test_app.server.test_client()
    yield _client

@pytest.fixture(scope='function')
def duo(dash_duo, test_app):
    """A client for the dash_duo/Flask tests."""
    dash_duo.driver.set_window_size(1500, 1200)
    dash_duo.driver.maximize_window()
    dash_duo.start_server(test_app)
    return dash_duo
