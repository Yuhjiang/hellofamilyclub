import os

from celery import Celery

profile = os.environ.get('HELLOFAMILYCLUB', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hellofamilyclub.settings.{}'.format(profile))

app = Celery('hellofamilyclub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
