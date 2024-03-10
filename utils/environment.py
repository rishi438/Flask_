import os

DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///sites.db")
TEMPLATES_AUTO_RELOAD = os.environ.get("TEMPLATES_AUTO_RELOAD", True)
CELERY_RABBITMQ_BROKER = os.environ.get(
    "CELERY_RABBITMQ_BROKER", 
    "pyamqp://guest:guest@localhost:5672//"
)
