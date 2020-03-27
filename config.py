import os


SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_ADDRESS = 'register@corona-meldung.de'
EMAIL_SMTP_SERVER = 'smtp.ionos.com'
EMAIL_SMTP_PASSWORD = os.environ.get('EMAIL_SMTP_PASSWORD')

ACCESS_TOKEN_EXPIRE_MINUTES = 300