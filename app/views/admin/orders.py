from flask import Blueprint, render_template
import sqlalchemy as sa

from app import db
from app.helpers.order_status import OrderStatus
from app.models import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/")
def orders():
    orders = db.session.scalars(
        sa.select(Order).where(
            Order.status == OrderStatus.sent and Order.status == OrderStatus.on_the_way
        )
    )
    other_orders = db.session.scalars(
        sa.select(Order).where(
            Order.status != OrderStatus.sent or Order.status != OrderStatus.on_the_way
        )
    )
    return render_template(
        "admin/orders.html", title="Orders", orders=orders, other_orders=other_orders
    )


@orders_bp.route("/<order_id>")
def order(order_id):
    order = db.first_or_404(sa.select(Order).where(Order.id == order_id))
    return render_template(
        "admin/order_preview.html",
        title=f"Order {order.created_at.strftime('%B %d, %Y')}",
        order=order,
    )


@orders_bp.route("/<order_id>/add_to_shopping")
def add_to_shopping(order_id):
    # add to shopping
    # update status to 'on the way'
    # redirect to order_preview
    pass


@orders_bp.route("/<order_id>/in_pickup_location")
def in_pickup_location(order_id):
    # remove from shopping
    # update to 'in pickup location'
    # redirect to order_preview
    pass


@orders_bp.route("/<order_id>/delivered")
def delivered(order_id):
    # update to delivered
    # redirect to order_preview
    pass


@orders_bp.route("/locations/<location_id>")
def orders_in_location(location_id):
    pass
