#!/bin/bash
PORT=$1
    
echo "starting migrate"
python manage.py migrate --settings "the_internet.settings"
echo "Done migrate"

echo "starting createsuperuser"
python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL --settings "the_internet.settings"
echo "Done createsuperuser"

gunicorn -w 3 -b :$PORT "the_internet.wsgi:application"
