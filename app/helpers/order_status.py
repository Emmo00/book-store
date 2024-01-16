from enum import Enum


class OrderStatus(Enum):
    cancelled = -1
    pending = 0
    sent = 1
    on_the_way = 2
    in_pickup_location = 3
    delivered = 4
