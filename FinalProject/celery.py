import os
import sys
from os import path

from celery import Celery

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CorporatePortal.settings')

app = Celery('CorporatePortal', broker='pyamqp://guest@localhost')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Create periodic tasks
# run celery beat: celery -A CorporatePortal beat -l info
# after run celery: celery -A CorporatePortal worker -l info -E
app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'testing.testing_logic.check_test_case_expired_date',
        'schedule': 15
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))