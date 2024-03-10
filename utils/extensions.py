from datetime import timedelta
from functools import wraps 


def context_app(app):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with app.app_context():
                return func(*args, **kwargs)
        return wrapper
    return decorator


def transform_datetime_ist(date_time):
    return date_time + timedelta(hours=5, minutes=30)