import pytest
from tests.admin import USER_NAME, USER_EMAIL, USER_PASSWORD, delete_user, css_id

from dash_spa import page_container

mail_args = {}

def test_register(mocker, spa, duo):

    # Test the registration UI and confirm that a verification
    # email is sent to the user

    login_manager = spa.server.login_manager

    if not login_manager.is_test():
        pytest.exit("You must be in test mode to run this test")

    # We must have an admin before regular users can register

    if login_manager.user_count() == 0:
        result = login_manager.add_user(name='Admin', password='1234', email='admin@test.com', role=['admin'])
        assert result

    # Delete the test user as preparation for test

    delete_user(login_manager, USER_EMAIL)

    # Mock the template emailer

    def mock_send(self, receiver, subject, test_mode=True):
        mail_args.update(self.args)
        mail_args['sender'] = 'test@pytest.com'
        mail_args['receiver'] = receiver
        mail_args['subject'] = subject

    mocker.patch('dash_spa_admin.template_mailer.TemplateMailer.send',mock_send)

    register_form = css_id('register')

    # Register new user confirm, via mock, that a registration email

    duo.server_url = duo.server_url + "/admin/register"
    result = duo.wait_for_text_to_equal(register_form.btn, "Register", timeout=20)
    assert result

    # Fill in the registration form

    name=duo.find_element(register_form.name)
    name.send_keys(USER_NAME)

    email=duo.find_element(register_form.email)
    email.send_keys(USER_EMAIL)

    password=duo.find_element(register_form.password)
    password.send_keys(USER_PASSWORD)

    confirm_password=duo.find_element(register_form.confirm_password)
    confirm_password.send_keys(USER_PASSWORD)

    if 'pages.terms_and_conditions' in page_container:
        terms=duo.find_element(register_form.terms)
        terms.click()

    # Submit the registration form and wait for the verify form to appear

    registration_submit = duo.find_element(register_form.btn)
    registration_submit.click()

    # Browser switching to verify code page ...

    verify_form = css_id('register_verify')

    result = duo.wait_for_text_to_equal(verify_form.btn, "Submit", timeout=20)
    assert result

    # Confirm the mailer mock has captured the email arguments

    assert mail_args['receiver'] == USER_EMAIL

    # Enter the verification code

    code=duo.find_element(verify_form.code)
    code.send_keys(mail_args['code'])

    verify_submit = duo.find_element(verify_form.btn)
    verify_submit.click()

    # Confirm redirect to login page

    login_form = css_id('login')

    result = duo.wait_for_text_to_equal(login_form.btn, "Sign In", timeout=20)
    assert result
