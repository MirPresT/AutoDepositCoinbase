import smtplib
import ssl
import json
from email.message import EmailMessage
from func.secrets_manager import get_secret

SMTP_PORT = 587
FROM_EMAIL = 'terrellvest@gmail.com'
APP_PASSWORD_SECRET_NAME = 'google_app_password'
TO_EMAIL = 'terrellvest+python_dev@gmail.com'


def email(subject, message, to=TO_EMAIL):
    # start server
    context = ssl.create_default_context()

    # login to server
    with smtplib.SMTP_SSL(
        host='smtp.gmail.com',
        port=465,
        context=context
    ) as server:
        # get gmail app password from aws secrets manager
        secret = get_secret(APP_PASSWORD_SECRET_NAME)
        app_password = secret[APP_PASSWORD_SECRET_NAME]

        server.login(user=FROM_EMAIL, password=app_password)

        # create a message
        message = f'{message}\n'

        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['From'] = 'terrell.vest@gmail.com'
        msg['To'] = to

        try:
            server.send_message(msg)
        except smtplib.SMTPRecipientsRefused as e:
            print(f"\nSMTP Recipients Refused: {to}\n{e}\n")
        except smtplib.SMTPSenderRefused as e:
            print(f"\nSender address refused: {msg['From']}\n{e}\n")
        except smtplib.SMTPDataError as e:
            print(f"\nThe SMTP server refused to accept the message data: {msg}\n{e}\n")