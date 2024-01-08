from flask import Blueprint, render_template

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/", strict_slashes=False)
def orders():
    return render_template("orders.html")


@orders_bp.route("/<order_id>", strict_slashes=False)
def order(order_id):
    return render_template("order_preview.html")
