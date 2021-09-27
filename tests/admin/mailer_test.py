from admin.template_mailer import TemplateMailer
from admin.login_manager import VERIFICATION_TEMPLATE

def test_send():
    name = 'Big Joe'
    code = 'ABCD'
    email = 'bigjoe@bigjoe.com'
    sender = 'admin@mailhoast.com'
    mailer = TemplateMailer(VERIFICATION_TEMPLATE, {'name' : name, 'code': code})
    email = mailer.send(sender, email, 'Password verification')
    assert code in email
