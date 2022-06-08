import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsboard.settings')
 
app = Celery('newsboard')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'week_sender_every_monday': {
        'task': 'newsportal.tasks.week_sender',
        'schedule': crontab(hour=12, minute=0, day_of_week='monday'),
    },
}