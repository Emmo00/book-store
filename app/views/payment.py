from flask import Blueprint, request, render_template, url_for, abort, redirect
import sqlalchemy as sa

from app import db
from app.models import Order
from app.helpers.payment import confirm_transaction
from app.helpers.order_status import OrderStatus, update_order

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/payment-complete")
def payment_complete():
    status = request.args.to_dict().get("status")
    order_id = request.args.to_dict().get("tx_ref")
    if status == "successful":
        if confirm_transaction():
            update_order(order_id, status=OrderStatus.sent)
        order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
        if not order:
            abort(404)
        return redirect(url_for("client.orders.order", order_id=order_id))
    update_order(order_id, status=OrderStatus.cancelled)
    return redirect(url_for("client.orders.order", order_id=order_id))
