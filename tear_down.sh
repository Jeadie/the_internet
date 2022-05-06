
# kill -9 $(ps | grep " python manage.py runserver" | cut -f1 -d " " | head -n 1)
kill -9 $(ps | grep celery | grep worker | cut -f1 -d " ") # Multiple worker processes possible
kill -9 $(ps | grep celery | grep beat | cut -f1 -d " " | head -n 1)
kill -9 $(ps | grep "/usr/local/sbin/rabbitmq-server" | cut -f1 -d " " | head -n 1)
