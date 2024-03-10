import time
from celery.schedules import crontab
from app_build import create_app
from api.models import db, Orders, Merchant
from sqlalchemy import func,desc
from celery.utils.log import get_task_logger
from utils.extensions import context_app
from sqlalchemy.exc import SQLAlchemyError


logger = get_task_logger(__name__)
app, celery = create_app()


def init_celery(celery):
    """ Celery Schedulers configuration

    Args:
        celery (object): celery instance

    Returns:
        object : configured celery
    """    
    celery.conf.beat_schedule = {
        "top-merchants": {
            "task": "api.tasks.rerank_merchants",
            "schedule": crontab(hour="*", minute="*"),
        },
    }
    celery.conf.enable_utc = False
    celery.conf.timezone = "Asia/Kolkata"
    return celery


@celery.task
@context_app(app)
def rerank_merchants():
    """Reranking Merchants
    """    
    try:
        logger.info("Rerank merchants is in progress")
        merchant_orders = db.session.query(
            Orders.merchant_id,
            func.count(Orders.id)
        ).group_by(Orders.merchant_id).order_by(
            desc(func.count(Orders.id))
        ).all()

        logger.info(f"sim {merchant_orders}")
        rankings = []
        for rank ,merchant_id in enumerate(merchant_orders):
            rankings.append((merchant_id,rank+1),)
        top_merchants = rankings[:10]
        logger.info(f"Rerank merchants {top_merchants}")

        for merchant,rank in top_merchants:
            update_merchant_rank(merchant[0], rank)
    except Exception as ex:
        logger.error(f"Error Occured in tasks.rerank_merchants: {ex}")


@celery.task
@context_app(app)
def order_populate(data):
    """Populating orders

    Args:
        data (object): populating

    Returns:
        Bool : Operation status
    """    
    try:
        time.sleep(15)
        order = Orders(**data)
        if order: 
            db.session.add(order)
            db.session.commit()
            return True
    except SQLAlchemyError as ex:
        print(f"Database Error in tasks.order_populate: {ex}")
    return False
    
    
def update_merchant_rank(merchant_id, rank):
    """Updating merchant ranking to DB

    Args:
        merchant_id (uuid): id of the merchant
        rank (int): rank of the merchant
    """    
    try:
        merchant = Merchant.query.get(merchant_id)
        merchant.rank = rank
        db.session.commit()
    except SQLAlchemyError as ex:
        logger.error("Error Occurred in tasks.update_merchant_rank: ", ex)