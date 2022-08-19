import logging
import pytest
from selenium.webdriver.chrome.options import Options


from dash.testing.composite import DashComposite
from dash.testing.application_runners import ThreadedRunner

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

    # https://stackoverflow.com/a/67222761/489239

    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    return options

# https://flask.palletsprojects.com/en/1.1.x/api/#flask.testing.FlaskClient
# https://stackoverflow.com/a/62379417/489239

# @pytest.fixture(scope='function')
# def test_client(test_app):
#     """A client for the Flask tests."""
#     _client = test_app.server.test_client()
#     yield _client


# @pytest.fixture(scope="module")
# def xdash_duo(request):
#     runner = ThreadedRunner()
#     with DashComposite(
#         runner,
#         browser=request.config.getoption("webdriver"),
#         remote=request.config.getoption("remote"),
#         remote_url=request.config.getoption("remote_url"),
#         headless=request.config.getoption("headless"),
#         options=request.config.hook.pytest_setup_options(),
#         download_path=None,
#         percy_assets_root=request.config.getoption("percy_assets"),
#         percy_finalize=request.config.getoption("nopercyfinalize"),
#         pause=request.config.getoption("pause"),
#     ) as duo:
#         yield duo

#     try:
#         runner.stop()
#     except:
#         pass

@pytest.fixture
def duo(dash_duo, test_app):
    """A client for the dash_duo/Flask tests."""
    dash_duo.driver.set_window_size(1500, 1200)
    # dash_duo.driver.maximize_window()
    dash_duo.start_server(test_app)
    return dash_duo
