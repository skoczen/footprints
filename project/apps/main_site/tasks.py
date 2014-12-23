import datetime
import requests

from celery.task import task, periodic_task
from django.conf import settings
from django.core.urlresolvers import reverse

@periodic_task(run_every=datetime.timedelta(seconds=60))
def keepalive():
    print "yo, it's %s" % datetime.datetime.now()
    r = requests.get("%s%s" % (settings.BASE_URL, reverse("main_site:ping")))
    print "Got: %s" % r.status_code