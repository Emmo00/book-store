from enum import Enum


class OrderStatus(Enum):
    sent = 0
    on_the_way = 1
    in_pickup_location = 2
    delivered = 3
