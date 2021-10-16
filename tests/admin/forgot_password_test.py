from tests.admin import USER_EMAIL


NEW_PASSWORD = 'bigjoe66'

mail_args = {}

def test_admin_forgot(mocker, duo):

    # Mock the template emailer

    def mock_send(self, sender, receiver, subject, test_mode):
        mail_args.update(self.args)
        mail_args['sender'] = sender
        mail_args['receiver'] = receiver
        mail_args['subject'] = subject
        mail_args['code'] = self.args['code']

    mocker.patch('dash_spa.admin.template_mailer.TemplateMailer.send', mock_send)

    # Mock password changer

    def mock_change_password(self, email, password):
        mail_args['new_password'] = password
        return True

    mocker.patch('dash_spa.admin.login_manager.AdminLoginManager.change_password', mock_change_password)

    # Render the forgot password page, enter the test user email.

    duo.server_url = duo.server_url + "/admin/forgot"

    result = duo.wait_for_text_to_equal("#admin-forgot-btn", "Reset Request", timeout=20)
    assert result

    email=duo.find_element("#admin-forgot-email")
    email.send_keys(USER_EMAIL)

    forgot_btn = duo.find_element("#admin-forgot-btn")
    forgot_btn.click()

    # A verification code is sent by email, this is intercepted
    # by TemplateMailer.mock_send(). The user is automatically redirected to
    # the verification code page.


    # Enter verification code

    result = duo.wait_for_text_to_equal("#admin-forgot1-btn", "Enter Verification Code", timeout=20)
    assert result

    code_input=duo.find_element("#admin-forgot1-code")
    code_input.send_keys(mail_args['code'])

    reset_btn=duo.find_element("#admin-forgot1-btn")
    reset_btn.click()

    # If the verification code checks out the user is redirected to the password
    # reset page

    result = duo.wait_for_text_to_equal("#admin-forgot2-btn", "Update Password", timeout=20)
    assert result

    # Enter the new password.

    password=duo.find_element("#admin-forgot2-password")
    password.send_keys(NEW_PASSWORD)

    confirm_password=duo.find_element("#admin-forgot2-confirm_password")
    confirm_password.send_keys(NEW_PASSWORD)

    reset_btn=duo.find_element("#admin-forgot2-btn")
    reset_btn.click()

    # If new password is accepted the user is redirected to the login page.

    result = duo.wait_for_text_to_equal("#admin-loginfrm-btn", "Sign In", timeout=20)
    assert result
