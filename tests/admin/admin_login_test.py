from itsdangerous import base64_decode
import zlib
from tests.admin import USER_NAME, USER_EMAIL, USER_PASSWORD, delete_user, css_id


# https://github.com/noraj/flask-session-cookie-manager/blob/master/flask_session_cookie_manager3.py
# https://www.kirsle.net/wizards/flask-session.cgi#source

def decode(cookie):
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = cookie

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)


def test_login(duo, test_app):

    login_manager = test_app.server.login_manager

    # Delete the test user as preparation for test

    delete_user(login_manager, USER_EMAIL)

    result = login_manager.add_user(name=USER_NAME, password=USER_PASSWORD, email=USER_EMAIL)
    assert result

    duo.driver.delete_all_cookies()

    # Login known user - confirm success

    duo.server_url = duo.server_url + "/admin/login"

    form = css_id('login')

    result = duo.wait_for_text_to_equal(form.btn, "Sign In", timeout=20)
    assert result

    email=duo.find_element(form.email)
    email.send_keys(USER_EMAIL)

    password=duo.find_element(form.password)
    password.send_keys(USER_PASSWORD)

    btn = duo.find_element(form.btn)
    btn.click()

    result = duo.wait_for_text_to_equal("#user-name", "Big Joe", timeout=20)
    assert result

    # Confirm flask_login.login_user() has been called and the session cookies
    # have been created.

    cookies = duo.driver.get_cookie('session')
    assert cookies

    session = decode(cookies['value'])
    assert '_id' in session


def test_admin_login_fail(duo, test_app):

    # Login known user with a bad password - confirm rejection
    #
    # Rejection results in a red flash up field being displayed inviting the user
    # to re-enter the user details.

    duo.server_url = duo.server_url + "/admin/login"

    form = css_id('login')

    btn = duo.find_element(form.btn)
    assert btn.text == "Sign In"

    email=duo.find_element(form.email)
    email.send_keys(USER_EMAIL)

    password=duo.find_element(form.password)
    password.send_keys('bad')

    btn.click()

    result = duo.wait_for_text_to_equal(form.flash, "Please check your login details and try again.", timeout=20)
    assert result
