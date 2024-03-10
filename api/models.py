from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db=SQLAlchemy()


class Merchant(db.Model):
    """Merchant schema

    Args:
        db.Model (object): The base class for Merchant model.
    """    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(36), nullable=False)
    address = db.Column(db.String(36), nullable=False)
    rank = db.Column(db.Integer, nullable=False, default=0)
    last_modified = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)


class Orders(db.Model):
    """Orders schema

    Args:
        db.Model (object): The base class for Orders model.
    """    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    merchant_id = db.Column(db.String(36), db.ForeignKey("merchant.id"), nullable=False)
    product_name = db.Column(db.String(36), nullable=False)
    address = db.Column(db.String(36), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
