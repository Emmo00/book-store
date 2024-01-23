from flask import Blueprint, render_template, session
import sqlalchemy as sa

from app import db
from app.models import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/", strict_slashes=False)
def orders():
    orders = db.session.scalars(
        sa.select(Order).where(Order.customer_id == session.get("user_id"))
    )
    return render_template("orders.html", title="Orders", orders=orders)


@orders_bp.route("/<order_id>", strict_slashes=False)
def order(order_id):
    order = db.first_or_404(sa.select(Order).where(Order.id == order_id))
    return render_template(
        "order_preview.html",
        title=f"Order on {order.created_at.strftime('%d-%m-%Y')}",
        order=order,
    )
