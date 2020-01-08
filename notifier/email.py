import smtplib
import ssl
from email.mime.text import MIMEText
from util import create_logger
from util.config import config


class Email:
    def __init__(self):
        self.logger = create_logger(msg='Email part')

    def send_email(self, mail, message):
        self.logger.info('Sending Email')

        port = config['mail'].get('port')
        smtp_server = config['mail'].get('server')
        sender_email = config['mail'].get('sender')
        receiver_email = mail
        password = config['mail'].get('passw')
        subject = 'Subject: Airtime of your TV shows\n'
        body = f'Hello,\n{message}'
        content = subject + MIMEText(body, 'plain').as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, content)
