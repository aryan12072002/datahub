import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datahub.settings')

app = Celery('datahub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'aggregate-every-30-minutes': {
        'task': 'aggregator.tasks.aggregate_all_sources',
        'schedule': 30 * 60.0,
    },
}
