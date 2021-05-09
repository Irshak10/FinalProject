web: gunicorn FinalProject.wsgi --log-file -
worker: celery -A FinalProject worker --beat --loglevel=info
