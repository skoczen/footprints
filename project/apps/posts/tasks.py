import datetime
from celery.task import task, periodic_task


@periodic_task(run_every=datetime.timedelta(seconds=5))
def test_task():
    print "yo, it's %s" % datetime.datetime.now()