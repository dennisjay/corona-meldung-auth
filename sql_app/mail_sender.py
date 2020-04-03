import smtplib
import ssl

import config

context = ssl.create_default_context()


def send_register_mail(receiver_email, token):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")
    message["Subject"] = "Dein Code zur Aktivierung des Accounts auf corona-meldung.de"
    message["From"] = config.EMAIL_ADDRESS
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hallo {},
    
    vielen Dank für dein Vertrauen in https://www.corona-meldung.de .
    
    Dein Code zur Aktivierung deines Accounts: {}
    """.format(receiver_email, token)
    html = """\
    <html>
      <body>
        <p>Hallo {},<br/><br/>
           vielen Dank für dein Vertrauen in https://www.corona-meldung.de .<br/><br/>
           Dein Code zur Aktivierung deines Accounts: <b>{}</b>
        </p>
      </body>
    </html>
    """.format(receiver_email, token)

    # Turn these into plain/html MIMEText objects
    text_content = MIMEText(text, "plain")
    html_content = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(text_content)
    message.attach(html_content)

    with smtplib.SMTP_SSL(config.EMAIL_SMTP_SERVER, 465, context=context) as server:
        server.login(config.EMAIL_USER_NAME, config.EMAIL_SMTP_PASSWORD)
        server.sendmail(
            config.EMAIL_ADDRESS, receiver_email, message.as_string()
        )


def send_login_mail(receiver_email, token):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ihr Code zum Login bei https://www.corona-meldung.de"
    message["From"] = config.EMAIL_ADDRESS
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hallo {},

    Ihr Code zum Login bei https://www.corona-meldung.de :
    
    Code: {}
    """.format(receiver_email, token)
    html = """\
    <html>
      <body>
        <p>Hallo {},<br>
           Ihr Code zum Login bei https://www.corona-meldung.de :<br/><br/>
           Code: {}
        </p>
      </body>
    </html>
    """.format(receiver_email, token)

    # Turn these into plain/html MIMEText objects
    text_content = MIMEText(text, "plain")
    html_content = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(text_content)
    message.attach(html_content)

    with smtplib.SMTP_SSL(config.EMAIL_SMTP_SERVER, 465, context=context) as server:
        server.login(config.EMAIL_USER_NAME, config.EMAIL_SMTP_PASSWORD)
        server.sendmail(
            config.EMAIL_ADDRESS, receiver_email, message.as_string()
        )

if __name__ == '__main__':
    send_login_mail(  'djprivat@gmail.com', 'hello world');
    send_register_mail(  'djprivat@gmail.com', 'hello world 2');