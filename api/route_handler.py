from .models import Orders,Merchant,db
from .tasks import order_populate
from flask import Blueprint, jsonify, request
from sqlalchemy import asc
from utils.constants import API_RESPONSE_OBJ, OrderStatus
from utils.extensions import transform_datetime_ist

api_routes = Blueprint("api",__name__)


@api_routes.route("/add-merchant",methods=["POST"])
def add_merchant():
    """Adding Merchant details 

    Returns:
        object : returns operation details
    """
    response = API_RESPONSE_OBJ.copy()    
    response["msg"] = "Error Occured!"
    try:
        data = request.get_json() or {}
        merchant = Merchant(**data)
        if merchant: 
            db.session.add(merchant)
            db.session.commit()
            response["msg"] = "Added Successfully"
            response["status"] = True
    except Exception as ex:
        print(f"Error Occurred route_handler.add_merchant: {ex}")
    return jsonify(response)


@api_routes.route("/add-order",methods=["POST"])
def add_order():
    """Adding Orders details

    Returns:
        object : returns operation details
    """  
    response = API_RESPONSE_OBJ.copy()    
    response["msg"] = "Error Occured!" 
    try:
        data = request.get_json() or {}
        data["status"] = OrderStatus[data["status"]].value
        result = order_populate.delay(data)
        if result:
            response["status"] = True
            response["msg"] = "Order added Successfully"
    except Exception as ex:  
        print(f"Error Occurred route_handler.add_order: {ex}")
        
    return jsonify(response)


@api_routes.route("/all-orders",methods=["GET"])
def orders():
    """All Orders details

    Returns:
        object : returns operation details
    """    
    response = API_RESPONSE_OBJ.copy()    
    response["msg"] = "Error Occured!" 
    try:
        data = db.session.query(Orders).all()
        if data:
            all_orders = []
            for order in data:
                order_dict = {
                    "id": order.id,
                    "merchant_id": order.merchant_id,
                    "product_name": order.product_name,
                    "address": order.address,
                    "status": OrderStatus(order.status).name,
                    "last_modified": transform_datetime_ist(order.last_modified).isoformat(),
                    "created_date": transform_datetime_ist(order.created_date).isoformat(),
                }
                all_orders.append(order_dict)
            if all_orders:
                response["msg"] = "Fetched orders successfully"
                response["status"] = True
                response["payload"] = all_orders
    except Exception as ex:
        print(f"Error Occurred route_handler.orders: {ex}")
    return jsonify(response)


@api_routes.route("/get-top-ten",methods=["GET"])
def merchants():
    """Top 10 Merchant details

    Returns:
        object : returns operation details
    """ 
    response = API_RESPONSE_OBJ.copy()    
    response["msg"] = "Error Occured!"
    try:
        data = db.session.query(
                Merchant
        ).filter(
            Merchant.rank > 0
        ).order_by(
            asc(Merchant.rank)
        ).limit(
            10
        )
        merchants_list = []
        for merchant in data:
            merchant_dict = {
                'id': merchant.id,
                'name': merchant.name,
                "rank":merchant.rank
            }
            merchants_list.append(merchant_dict)
        if merchants_list:
            response["msg"] = "Order added Successfully"
            response["status"] = True
            response["payload"] = merchants_list
    except Exception as ex:
        print(f"Error Occurred route_handler.merchants: {ex}")
    return jsonify(response)