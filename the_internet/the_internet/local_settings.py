import os

from the_internet.settings import BASE_DIR

SECRET_KEY = 'django-insecure-h*(16ugbn%yv_$@02=%r_@-s1kcfbyzxdx)7=9okcyb9p#+7p-'
DEBUG=True

CSRF_TRUSTED_ORIGINS = ["https://*", "http://*", "http://0.0.0.0:1337"]

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}