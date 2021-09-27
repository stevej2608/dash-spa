
from tests.admin import USER_NAME, USER_EMAIL, USER_PASSWORD, delete_user

def test_admin_login(duo, spa):

    login_manager = spa.login_manager

    # Delete the test user as preparation for test

    delete_user(login_manager, USER_EMAIL)

    result = login_manager.add_user(name=USER_NAME, password=USER_PASSWORD, email=USER_EMAIL)
    assert result

    # Login known user - confirm success

    duo.server_url = duo.server_url + "/admin/login"

    result = duo.wait_for_text_to_equal("#admin-login-form-btn", "Sign In", timeout=20)
    assert result

    email=duo.find_element("#admin-login-form-email")
    email.send_keys(USER_EMAIL)

    password=duo.find_element("#admin-login-form-password")
    password.send_keys(USER_PASSWORD)

    btn = duo.find_element("#admin-login-form-btn")
    btn.click()

    result = duo.wait_for_text_to_equal("#user-profile-name", "Big Joe", timeout=20)
    assert result

def test_admin_login_fail(duo):

    # Login known user with a bad password - confirm rejection
    #
    # Rejection results in a red flash up field being displayed inviting the user
    # to re-enter the user details.

    duo.server_url = duo.server_url + "/admin/login"

    btn = duo.find_element("#admin-login-form-btn")
    assert btn.text == "Sign In"

    email=duo.find_element("#admin-login-form-email")
    email.send_keys(USER_EMAIL)

    password=duo.find_element("#admin-login-form-password")
    password.send_keys('bad')

    btn.click()

    result = duo.wait_for_text_to_equal("#admin-login-form-flash", "Please check your login details and try again.", timeout=20)
    assert result
