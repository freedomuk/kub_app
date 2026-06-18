from celery import Celery

celery_app = Celery(
    'worker',
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Kyiv",
    enable_utc=True,
    worker_prefetch_multiplier = 1,
    task_defual_queue = 'default',
    # task_queues={
    #     'python':{
    #         'exchange':'python',
    #         'routing_key':'python'
    #     },
    #     'js':{
    #         'exchange':'js',
    #         'routing_key':'js'
    #     }
    # }
)

import tasks