import os
import sys
from os import path

from celery import Celery

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')

app = Celery('FinalProject')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Create periodic tasks
app.conf.beat_schedule = {
    'every-1-hour': {
        'task': 'testing.testing_logic.check_expired_test_date',
        'schedule': 3600
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# celery -A FinalProject worker --beat --loglevel=info
