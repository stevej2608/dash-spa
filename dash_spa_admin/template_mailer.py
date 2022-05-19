import pystache
import smtplib
from email.mime.text import MIMEText

from dash_spa import config
from dash_spa.logging import log

header_template = """
Subject: {{subject}}
To: {{receiver}}
From: {{sender}}
"""

class TemplateMailer:

    def __init__(self, template, args):
        self.options = config.get('login_manager.mail')
        self.args = args
        self.email_msg = pystache.render(template, args)

    @property
    def smt_transport(self):
        options = self.options
        if options.secure:
            return smtplib.SMTP_SSL(options.host, options.port)
        else:
            return smtplib.SMTP(options.host, options.port)

    def send(self, receiver, subject, test_mode=True):
        options = self.options
        sender = options.sender

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
                server.login(options.user, options.password)
                server.send_message(msg)
                log.info('Done')

        except Exception as ex:
            log.info('email send failed %s', ex)
