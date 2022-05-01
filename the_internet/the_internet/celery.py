import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "the_internet.settings")

app = Celery("the_internet")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
