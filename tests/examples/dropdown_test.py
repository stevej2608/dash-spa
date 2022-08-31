import time
from selenium.common.exceptions import TimeoutException
import pytest
from dash import html, ALL
from dash_spa import  match, prefix

from examples.button_dropdown.app import create_dash, create_app


@pytest.fixture
def test_app():
    spa = create_app(create_dash)
    yield spa


def test_dropdown_select(duo, test_app):

    duo.server_url = duo.server_url + "/"

    # Confirm page is showing

    result = duo.wait_for_text_to_equal("#test_h4", "Page size is 10", timeout=20)
    assert result

    # Open the dropdown

    dropdown_button = duo.find_element("#test_settings_dropdown_btn")
    dropdown_button.click()

    # Confirm dropdown is open

    result = duo.wait_for_text_to_equal('.dropdown-item', '10', timeout=20)
    assert result is True

    # Click the last element in the dropdown

    btn = duo.find_elements('.dropdown-item')[2]
    btn.click()

    result = duo.wait_for_text_to_equal("#test_h4", "Page size is 30", timeout=20)
    assert result


def test_dropdown_cancel(duo, test_app):

    duo.server_url = duo.server_url + "/"

    # Confirm page is showing

    result = duo.wait_for_text_to_equal("#test_h4", "Page size is 10", timeout=20)
    assert result

    # Open the dropdown

    dropdown_button = duo.find_element("#test_settings_dropdown_btn")
    dropdown_button.click()

    # Confirm dropdown is open

    result = duo.wait_for_text_to_equal('.dropdown-item', '10', timeout=20)
    assert result is True

    # Click the banner (could use any element outside the drop down)

    h4 = duo.find_element('#test_h4')
    h4.click()

    # Wait for drop down to close

    time.sleep(1)

    # Confirm that drop down items are no longer visible

    with pytest.raises(TimeoutException) as error:
        duo.wait_for_text_to_equal('.dropdown-item', '10', timeout=2)
