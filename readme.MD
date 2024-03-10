pip install -r requirements.txt


# Run Server
python server.py

# Run Celery Scheduler and Celery Worker
celery -A server.celery_scheduler worker --pool=solo -l info
celery -A server.celery_scheduler beat -l info

# Run Check Status of tasks
celery -A server.celery_scheduler flower