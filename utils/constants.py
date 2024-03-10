from enum import unique,IntEnum


RESPONSE_STATUS = "status"
RESPONSE_MSG = "msg"
API_RESPONSE_OBJ = {
    RESPONSE_STATUS: False,
    RESPONSE_MSG: "TODO",
}

@unique
class OrderStatus(IntEnum):
    ORDERED = 0
    SHIPPED = 1
    OUT_FOR_DELIEVERY = 2
    DELIEVERED = 3
    RETRY_DELIEVERY = 4
    RETURNED = 5
    
