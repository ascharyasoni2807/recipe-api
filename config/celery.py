# celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-daily-notifications': {
        'task': 'recipe.tasks.send_daily_notifications',
        'schedule': crontab(hour="0", minute="0"),
    },
}
# change this to for getting email in every one minute
# 'schedule': crontab(hour="*", minute="*/1"),