from examples.redirect import create_app

def test_redirect(dash_duo):

    app = create_app().init()
    dash_duo.start_server(app)
    dash_duo.server_url = dash_duo.server_url + '/test/page1'

    # https://dash.plot.ly/testing
    # https://www.testingexcellence.com/css-selectors-selenium-webdriver/
    # https://www.w3schools.com/cssref/css_selectors.asp

    # dash_duo.wait_for_element("style='display:block;'", timeout=30)
    dash_duo.wait_for_style_to_equal("#spa-router-test-page1", "display", "block", timeout=30)

    webelement = dash_duo.find_element("#test-page1-btn")
    assert webelement.is_displayed()
