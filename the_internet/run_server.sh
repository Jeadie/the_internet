#!/bin/bash
PORT=$1

export STAGE="local"
python manage.py migrate

export DJANGO_SUPERUSER_USERNAME="duck_admin"
export DJANGO_SUPERUSER_PASSWORD="test"
export DJANGO_SUPERUSER_EMAIL="jackeadie+1@duck.com"

python manage.py createsuperuser --noinput

gunicorn -w 3 -b :$PORT "the_internet.wsgi:application"
