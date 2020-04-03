import os


SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_ADDRESS = 'register@corona-meldung.de'
EMAIL_SMTP_SERVER = 'email-smtp.eu-central-1.amazonaws.com'
EMAIL_USER_NAME = os.environ.get('EMAIL_USER_NAME')
EMAIL_SMTP_PASSWORD = os.environ.get('EMAIL_SMTP_PASSWORD')
MYSQL_CONNECTION_URL = os.environ.get('MYSQL_CONNECTION_URL')
POSTGRES_CONNECTION_URL = os.environ.get('DATABASE_URL')


ACCESS_TOKEN_EXPIRE_MINUTES = 300