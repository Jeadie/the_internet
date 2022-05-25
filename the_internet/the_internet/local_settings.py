from the_internet.settings import BASE_DIR

SECRET_KEY = 'django-insecure-h*(16ugbn%yv_$@02=%r_@-s1kcfbyzxdx)7=9okcyb9p#+7p-'
DEBUG=True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}