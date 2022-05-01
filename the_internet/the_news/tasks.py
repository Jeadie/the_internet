from celery import shared_task

@shared_task
def debug_task(data: Dict[object, object]):
    print(f'data: {data!r}')