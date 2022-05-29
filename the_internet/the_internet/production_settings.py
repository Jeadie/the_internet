import os


""" Secrets that must be passed into django server
 - DJANGO_SECRET_KEY
 - RDS_DB_NAME
 - RDS_USERNAME
 - RDS_PASSWORD

 Settings that are not secret, but environment dependent:
  - RDS_HOSTNAME
  - RDS_PORT
  - ALLOWED_HOSTS (Eventually)
"""

DEBUG=False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# ALLOWED_HOSTS = ["the-internet-server.eba-tasfmrba.us-east-1.elasticbeanstalk.com", "news.onceaday.fyi", "onceaday.fyi"]
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
}