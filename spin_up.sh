
source .venv/bin/activate
cd the_internet/

# rabbitmq server message queue, cron scheduler and task worker processes
/usr/local/sbin/rabbitmq-server > ../logs/ampq.log & 
celery -A the_internet beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler > ../logs/celery-beat.log & 
celery --app=the_internet worker > ../logs/celery-worker.log & 


# python manage.py runserver > ../logs/django-server & 

echo "Everything happily running..."