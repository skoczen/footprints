web: newrelic-admin run-program python manage.py run_gunicorn -b '0.0.0.0:$PORT' --workers=4 --settings=envs.live
celery: newrelic-admin run-program python manage.py celeryd -c 3 -B --settings=envs.live
