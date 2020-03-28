import smtplib
import ssl

import config

context = ssl.create_default_context()


def send_register_mail(receiver_email, token):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = config.EMAIL_ADDRESS
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hallo {},
    
    vielen Dank für Ihr Vertrauen in https://www.corona-meldung.de .
    
    Ihr 4-stelliger Code zur Aktivierung ihres Accounts: {}
    """.format(receiver_email, token)
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL(config.EMAIL_SMTP_SERVER, 465, context=context) as server:
        server.login(config.EMAIL_ADDRESS, config.EMAIL_SMTP_PASSWORD)
        server.sendmail(
            config.EMAIL_ADDRESS, receiver_email, message.as_string()
        )

if __name__ == '__main__':
    send_register_mail("djprivat@gmail.com", "TEST")
