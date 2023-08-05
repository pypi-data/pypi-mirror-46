#coding: utf-8 
from __future__ import print_function, unicode_literals

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class Email():
    ALLOW_FORMAT = ['plain', 'html']

    def __init__(self, smtp_name='smtp.gmail.com', smtp_port=587, login_name=None, login_pwd=None):
        """
        Init smtp to send email from email client
        :param smtp_name:
        :param smtp_port:
        :param login_name:
        :param login_pwd:
        """
        self.smtp_name = smtp_name
        self.smtp_port = smtp_port
        self.login_name = login_name
        self.login_pwd = login_pwd

    def test_package(self):
        print("It's work!")

    @staticmethod
    def check_require_info(*kwargs):
        for email_info in kwargs:
            if not email_info:
                raise ValueError('Please fill all from_address, to_address, subject and content')

    def send_mail(self, from_address, to, subject, content, cc=None, bcc=None, format_content='html', allow_retry_number=5):
        # validate params which required
        self.check_require_info(from_address, to, subject, content)

        # set receiver info
        rcpt = []
        if cc:
            rcpt += cc.split(",")
        if bcc:
            rcpt += bcc.split(",")
        rcpt = rcpt + [to]

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to
        if cc:
            msg['Cc'] = cc
        if bcc:
            msg['Bcc'] = bcc

        # Record the MIME types of both parts - text/plain and text/html.
        if format_content not in self.ALLOW_FORMAT:
            raise ValueError('Only accept content format: {}' . format(", ".join(self.ALLOW_FORMAT)))

        part = MIMEText(content, format_content)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part)

        # setup smtp and send mail
        print(self.smtp_name)
        print(self.smtp_port)
        retry_number = 0
        is_success = False
        error_msg = ""
        while(retry_number < allow_retry_number and not is_success):
            try:
                s = smtplib.SMTP(self.smtp_name, self.smtp_port)
                is_success = True
            except Exception as e:
                error_msg = str(e)
                retry_number += 1
           
        if is_success:  
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(self.login_name, self.login_pwd)
            s.sendmail(from_address, rcpt, msg.as_string())
            s.quit()
        else:
            print("send mail failed because of {}".format(error_msg))