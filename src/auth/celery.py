import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

if os.name == "nt":
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    
    
app = Celery('auth')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
@app.task()
def add(x,y):
    return x+y
