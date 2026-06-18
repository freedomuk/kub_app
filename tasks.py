from celery_app import celery_app
from celery.exceptions import SoftTimeLimitExceeded

@celery_app.task
def get():
    return 'Good'

@celery_app.task
def data(a:int,b:int):
    return a + b
