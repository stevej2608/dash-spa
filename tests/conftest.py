import logging
import pytest
from selenium.webdriver.chrome.options import Options

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

    # https://stackoverflow.com/a/67222761/489239

    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return options

@pytest.fixture
def duo(dash_duo, test_app):
    """A client for the dash_duo/Flask tests."""
    dash_duo.driver.set_window_size(1500, 1200)
    # dash_duo.driver.maximize_window()
    dash_duo.start_server(test_app)
    return dash_duo
