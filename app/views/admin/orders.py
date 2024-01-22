from flask import Blueprint, render_template, url_for, redirect
import sqlalchemy as sa

from app import db
from app.helpers.order_status import OrderStatus
from app.models import Order, Shopping, PickupLocation

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
    locations = db.session.scalars(sa.select(PickupLocation))
    return render_template(
        "admin/orders.html",
        title="Orders",
        orders=orders,
        other_orders=other_orders,
        locations=locations,
        location_id="",
    )


@orders_bp.route("/locations/<location_id>")
def orders_in_location(location_id):
    location = db.session.scalar(
        sa.select(PickupLocation).where(PickupLocation.id == location_id)
    )
    orders = db.session.scalars(
        sa.select(Order)
        .where(Order.pickup_location_id == location_id)
        .where(
            Order.status == OrderStatus.sent and Order.status == OrderStatus.on_the_way
        )
    )
    other_orders = db.session.scalars(
        sa.select(Order)
        .where(Order.pickup_location_id == location_id)
        .where(
            Order.status != OrderStatus.sent or Order.status != OrderStatus.on_the_way
        )
    )
    locations = db.session.scalars(sa.select(PickupLocation))
    return render_template(
        "admin/orders.html",
        title=f"Orders in {location.name}",
        orders=orders,
        other_orders=other_orders,
        locations=locations,
        location_id=location_id,
    )


@orders_bp.route("/<order_id>")
def order(order_id):
    order = db.first_or_404(sa.select(Order).where(Order.id == order_id))
    action = {
        OrderStatus.cancelled: {
            "text": "Canceled Order",
            "link": url_for("admin.orders.order", order_id=order_id),
        },
        OrderStatus.pending: {
            "text": "Pending order",
            "link": url_for("admin.orders.order", order_id=order_id),
        },
        OrderStatus.sent: {
            "text": "Add to shopping",
            "link": url_for("admin.orders.add_to_shopping", order_id=order_id),
        },
        OrderStatus.on_the_way: {
            "text": "In Pickup Location",
            "link": url_for("admin.orders.in_pickup_location", order_id=order_id),
        },
        OrderStatus.in_pickup_location: {
            "text": "Delivered?",
            "link": url_for("admin.orders.delivered", order_id=order_id),
        },
        OrderStatus.delivered: {
            "text": "Delivered",
            "link": url_for("admin.orders.order", order_id=order_id),
        },
    }
    return render_template(
        "admin/order_preview.html",
        title=f"Order {order.created_at.strftime('%B %d, %Y')}",
        order=order,
        action=action,
    )


@orders_bp.route("/<order_id>/add_to_shopping")
def add_to_shopping(order_id):
    order: Order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
    # add to shopping
    Shopping.add_order(order)
    # update status to 'on the way'
    order.status = OrderStatus.on_the_way
    db.session.add(order)
    db.session.commit()
    # redirect to order_preview
    return redirect(url_for("admin.orders.order", order_id=order_id))


@orders_bp.route("/<order_id>/in_pickup_location")
def in_pickup_location(order_id):
    order: Order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
    # remove from shopping
    Shopping.remove_order(order)
    # update to 'in pickup location'
    order.status = OrderStatus.in_pickup_location
    db.session.add(order)
    db.session.commit()
    # redirect to order_preview
    return redirect(url_for("admin.orders.order", order_id=order_id))


@orders_bp.route("/<order_id>/delivered")
def delivered(order_id):
    order: Order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
    # update to delivered
    order.status = OrderStatus.delivered
    db.session.add(order)
    db.session.commit()
    # redirect to order_preview
    return redirect(url_for("admin.orders.order", order_id=order_id))
