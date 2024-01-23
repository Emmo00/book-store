from flask import Blueprint, request, url_for, abort, redirect

from app.helpers.payment import confirm_transaction
from app.helpers.order_status import OrderStatus, update_order

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/payment-complete", strict_slashes=False)
def payment_complete():
    status = request.args.to_dict().get("status")
    order_id = request.args.to_dict().get("tx_ref")
    transaction_id = request.args.to_dict().get("transaction_id")
    if status == "successful":
        if confirm_transaction(transaction_id):
            update_order(order_id, status=OrderStatus.sent)
        return redirect(url_for("client.orders.order", order_id=order_id))
    update_order(order_id, status=OrderStatus.cancelled)
    return redirect(url_for("client.orders.order", order_id=order_id))
