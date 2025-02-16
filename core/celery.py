from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.conf.enable_utc = False
app.conf.update(timezone="Europe/London")

app.config_from_object(settings, namespace="CELERY")

app.conf.beat_schedule = {
    "updateCounterHistory": {
        "task": "apps.home.tasks.updateCounterHistory",
        # TODO: change for production release to new schedule
        "schedule": crontab(day_of_month=15),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
