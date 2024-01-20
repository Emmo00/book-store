from enum import Enum

import sqlalchemy as sa

from app import db


class OrderStatus(Enum):
    cancelled = -1
    pending = 0
    sent = 1
    on_the_way = 2
    in_pickup_location = 3
    delivered = 4


def update_order(order_id, status=OrderStatus.sent):
    from app.models import Order

    order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
    if not order:
        return
    order.status = status
    db.session.add(order)
    db.session.commit()
