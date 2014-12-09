import datetime
import requests
from celery.task import task, periodic_task
from django.conf import settings


@periodic_task(run_every=datetime.timedelta(seconds=30))
def keepalive():
    print "yo, it's %s" % datetime.datetime.now()
    r = requests.get(settings.PING_URL)
    print "Got: %s" % r.status_code