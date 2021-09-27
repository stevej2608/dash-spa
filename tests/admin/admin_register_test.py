from tests.admin import USER_NAME, USER_EMAIL, USER_PASSWORD, delete_user


mail_args = {}

def test_admin_register(mocker, spa, duo):

    # Test the registration UI and confirm that a verification
    # email is sent to the user

    login_manager = spa.login_manager

    # Delete the test user as preparation for test

    delete_user(login_manager, USER_EMAIL)

    # Mock the tempate emailer

    def mock_send(self, sender, receiver, subject, test_mode):
        mail_args.update(self.args)
        mail_args['sender'] = sender
        mail_args['receiver'] = receiver
        mail_args['subject'] = subject

    mocker.patch('admin.template_mailer.TemplateMailer.send',mock_send)

    # Register new user confirm, via mock, that a registration email

    duo.server_url = duo.server_url + "/admin/register"
    result = duo.wait_for_text_to_equal("#admin-register-btn", "Register", timeout=20)
    assert result

    # Fill in the form

    name=duo.find_element("#admin-register-name")
    name.send_keys(USER_NAME)

    email=duo.find_element("#admin-register-email")
    email.send_keys(USER_EMAIL)

    password=duo.find_element("#admin-register-password")
    password.send_keys(USER_PASSWORD)

    confirm_password=duo.find_element("#admin-register-confirm_password")
    confirm_password.send_keys(USER_PASSWORD)

    terms=duo.find_element("#admin-register-terms")
    terms.click()

    # Submit the registration form and wait for the verify form to appear

    registration_submit = duo.find_element("#admin-register-btn")
    registration_submit.click()

    result = duo.wait_for_text_to_equal("#admin-verify-btn", "Submit", timeout=20)
    assert result

    # Confirm the mock has captured the email arguments

    assert mail_args['receiver'] == USER_EMAIL

    # Wait for the verification page to appear

    verify_submit = duo.wait_for_text_to_equal("#admin-verify-btn", "Submit", timeout=20)
    verify_submit = duo.find_element("#admin-verify-btn")

    # Enter the verification code

    code=duo.find_element("#admin-verify-code")
    code.send_keys(mail_args['code'])

    verify_submit.click()

    # Confirm redirect to login page

    result = duo.wait_for_text_to_equal("#admin-login-form-btn", "Sign In", timeout=20)
    assert result
