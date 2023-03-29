import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')


app = Celery("app")


@app.task
def soma(x, y):
    return x + y
