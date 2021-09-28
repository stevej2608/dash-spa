

def test_page(duo, spa):

    # Login known user - confirm success

    duo.server_url = duo.server_url + "/demo/page1"

    result = duo.wait_for_text_to_equal("#page", "Page 1", timeout=20)
    assert result
