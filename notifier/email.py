import smtplib
import ssl
from email.mime.text import MIMEText
from util import create_logger


class Email:
    def __init__(self):
        self.logger = create_logger(msg='Email part')

    def send_email(self, mail, message):
        self.logger.info('Sending Email')

        port = 465  # For SSL
        smtp_server = 'smtp.gmail.com'
        sender_email = 'onurtest96@gmail.com'
        receiver_email = mail
        password = 'Onurtest1.'
        subject = "Subject: Airtime of your TV shows\n"
        body = f'Hello,\n{message}'
        content = subject + MIMEText(body, 'plain').as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, content)
