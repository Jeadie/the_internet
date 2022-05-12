import os

from base import * 


DEBUG=False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = ["the-internet-server.eba-tasfmrba.us-east-1.elasticbeanstalk.com", "news.onceaday.fyi", "onceaday.fyi"]