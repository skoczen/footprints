# -*- coding: utf-8 -*-
from multiprocessing import Process
import subprocess
import sys
import time
import os

if "PORT" in os.environ:
    port = os.environ["PORT"]
    settings = "--settings=envs.live"
else:
    settings = ""
    port = "8202"

command_config = {
    "settings": settings,
    "port": port,
}

class DjangoCelery(object):
    def bootstrap(self):
        print "bootstrapping"
        celery_thread = Process(target=self.bootstrap_celery)
        django_thread = Process(target=self.bootstrap_django)

        try:
            # Start up threads.
            celery_thread.start()
            django_thread.start()

            while True:
                time.sleep(100)

        except (KeyboardInterrupt, SystemExit):
            django_thread.terminate()
            celery_thread.terminate()
            print '\n\nReceived keyboard interrupt, quitting threads.',
            while django_thread.is_alive() or celery_thread.is_alive() or sys.stdout.write("."):
                sys.stdout.flush()
                time.sleep(0.5)
        except:
            import traceback; traceback.print_exc();

    def bootstrap_django(self):
        print "yo"
        subprocess.call("python manage.py run_gunicorn -b '0.0.0.0:%(port)s' --workers=4 %(settings)s" % command_config, shell=True)

    def bootstrap_celery(self):
        print "yep"
        subprocess.call("python manage.py celeryd -c 3 -B %(settings)s" % command_config, shell=True)
        

if __name__ == '__main__':
    instance = DjangoCelery()
    instance.bootstrap()
