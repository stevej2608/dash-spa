

def test_page_nav(duo, spa):

    duo.server_url = duo.server_url + "/demo/page1"

    # Confirm we're on page 1

    result = duo.wait_for_text_to_equal("#page", "Page 1", timeout=20)
    assert result

    # Switch to page 2 and confirm we're on it

    nav_link2 = duo.find_element("#nav-page2")
    nav_link2.click()
    result = duo.wait_for_text_to_equal("#page", "Page 2", timeout=20)
    assert result

    # Switch back to page 1 and confirm we're on it

    nav_link1 = duo.find_element("#nav-page1")
    nav_link1.click()
    result = duo.wait_for_text_to_equal("#page", "Page 1", timeout=20)
    assert result

    # Use history to return to page 2 and confirm we're on it

    duo.driver.back()
    result = duo.wait_for_text_to_equal("#page", "Page 2", timeout=20)
    assert result

    # Use history to return to page 1 and confirm we're on it

    duo.driver.forward()
    result = duo.wait_for_text_to_equal("#page", "Page 1", timeout=20)
    assert result

