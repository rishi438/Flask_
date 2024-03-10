from celery import Celery
from flask import Flask

from api.models import db
from utils.environment import (
    CELERY_RABBITMQ_BROKER,
    DATABASE_URI,
    TEMPLATES_AUTO_RELOAD,
)


def create_app():
    """Creates Web Server Application

    Returns:
        tuple: containing instances of app and celery
    """    
    
    app = Flask(__name__)

    celery = Celery(
        "app",
        broker=CELERY_RABBITMQ_BROKER,
        include=["api.tasks"]
    )
    celery.conf.update(app.config)
    
    app.config["TEMPLATES_AUTO_RELOAD"] = TEMPLATES_AUTO_RELOAD
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app, celery