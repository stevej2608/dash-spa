from tests.admin import USER_EMAIL

from tests.admin import css_id

NEW_PASSWORD = 'bigjoe66'

mail_args = {}

def test_admin_forgot(mocker, duo):

    # Mock the template emailer

    def mock_send(self, receiver, subject, test_mode=True):
        mail_args.update(self.args)
        mail_args['sender'] = 'test@pytest.com'
        mail_args['receiver'] = receiver
        mail_args['subject'] = subject
        mail_args['code'] = self.args['code']

    mocker.patch('dash_spa_admin.template_mailer.TemplateMailer.send', mock_send)

    # Mock password changer

    def mock_change_password(self, email, password):
        mail_args['new_password'] = password
        return True

    mocker.patch('dash_spa_admin.login_manager.AdminLoginManager.change_password', mock_change_password)

    # Render the forgot password page, enter the test user email.

    duo.server_url = duo.server_url + "/admin/forgot"

    forgot_form = css_id('forgot')

    result = duo.wait_for_text_to_equal(forgot_form.btn, "Reset Request", timeout=20)
    assert result

    email=duo.find_element(forgot_form.email)
    email.send_keys(USER_EMAIL)

    forgot_btn = duo.find_element(forgot_form.btn)
    forgot_btn.click()

    # A verification code is sent by email, this is intercepted
    # by TemplateMailer.mock_send(). The user is automatically redirected to
    # the verification code page.

    # Enter verification code

    forgot_code_form = css_id('forgot_code')

    result = duo.wait_for_text_to_equal(forgot_code_form.btn, "Enter Verification Code", timeout=20)
    assert result

    code_input=duo.find_element(forgot_code_form.code)
    code_input.send_keys(mail_args['code'])

    reset_btn=duo.find_element(forgot_code_form.btn)
    reset_btn.click()

    # If the verification code checks out the user is redirected to the password
    # reset page

    forgot_password_form = css_id('forgot_password')

    result = duo.wait_for_text_to_equal(forgot_password_form.btn, "Update Password", timeout=20)
    assert result

    # Enter the new password.

    password=duo.find_element(forgot_password_form.password)
    password.send_keys(NEW_PASSWORD)

    confirm_password=duo.find_element(forgot_password_form.confirm_password)
    confirm_password.send_keys(NEW_PASSWORD)

    reset_btn=duo.find_element(forgot_password_form.btn)
    reset_btn.click()

    # If new password is accepted the user is redirected to the login page.

    login_form = css_id('login')

    result = duo.wait_for_text_to_equal(login_form.btn, "Sign In", timeout=20)
    assert result
