import pystache
import smtplib
from email.mime.text import MIMEText

from utils import config, log

options = config.get('mail_options')
options = options.__getattribute__(options.active)

header_template = """
Subject: {{subject}}
To: {{receiver}}
From: {{sender}}
"""

class TemplateMailer:

    def __init__(self, template, args):
        self.args = args
        self.email_msg = pystache.render(template, args)

    @property
    def smt_transport(self):
        if options.secure:
            return smtplib.SMTP_SSL(options.host, options.port)
        else:
            return smtplib.SMTP(options.host, options.port)

    def send(self, sender, receiver, subject, test_mode=True):

        # When testing no email is sent. Instead we just print the
        # email that would have been sent

        if test_mode:
            args = locals()
            email = pystache.render(header_template + self.email_msg, args)
            print('Test mode: email send is dissabled.\nThe following email would have been sent:\n')
            print(email)
            return email

        try:
            msg = MIMEText(self.email_msg)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = receiver

            log.info('sending email to %s ...', receiver)
            with self.smt_transport as server:
                # server.ehlo()
                # server.starttls()
                server.login(options.auth.user, options.auth.password)
                server.send_message(msg)
                log.info('Done')

        except Exception as ex:
            log.info('email send failed %s', ex)
