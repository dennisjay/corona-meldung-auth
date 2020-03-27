import smtplib
from email.message import EmailMessage


def send_email(email_address: str, subject: str, msg: str):
    email = EmailMessage()
    email.set_content(msg)
    email['Subject'] = subject
    email['From'] = 'register@corona-meldung.de'
    email['To'] = email_address

    s = smtplib.SMTP('localhost')
    s.send_message(email)
    s.quit()
