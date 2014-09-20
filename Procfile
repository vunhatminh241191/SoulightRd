web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
scheduler: python manage.py celery worker -B -E --maxtasksperchild=1000
worker: python manage.py celery worker -E --maxtasksperchild=1000
collectstatic: python manage.py collectstatic
syncdb: python manage.py syncdb
migration: python manage.py migrate allauth.socialaccount && python manage.py migrate allauth.socialaccount.providers.facebook && python manage.py migrate djcelery && python manage.py migrate cities_light && python manage.py migrate main
build: python build.py prod 
rebuild_index: python manage.py rebuild_index