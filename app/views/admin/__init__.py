from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for, request
import sqlalchemy as sa

from .auth import auth_bp, logged_in
from .books import books_bp
from .orders import orders_bp
from .shopping import shopping_bp
from .withdraw import withdraw_bp
from .locations import location_bp

from app import db
from app.helpers.order_status import OrderStatus
from app.models import Order, Book, BookOrder, PickupLocation, Customer


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_bp.route("/home")
@admin_bp.route("/dashboard")
def index():
    stats = {}
    query = (
        sa.select(sa.func.count())
        .select_from(Order)
        .where(
            Order.status == OrderStatus.pending
            or Order.status == OrderStatus.on_the_way
        )
    )
    stats["pending_orders"] = db.session.scalar(query)

    query = sa.select(sa.func.count()).select_from(Book)
    stats["books"] = db.session.scalar(query)

    stats["shopping_list_count"] = db.session.scalar(query)

    query = sa.select(sa.func.count()).select_from(PickupLocation)
    stats["locations"] = db.session.scalar(query)

    now = datetime.now()
    month_begin = now - timedelta(
        days=now.day - 1, hours=now.hour, minutes=now.minute, seconds=now.second
    )
    query = (
        sa.select(sa.func.count())
        .select_from(Customer)
        .where(Customer.created_at >= month_begin)
    )
    stats["new_customers"] = db.session.scalar(query)

    previous_month = month_begin - timedelta(days=30)
    print(month_begin, previous_month)
    query = (
        sa.select(sa.func.count())
        .select_from(Customer)
        .where(Customer.created_at >= previous_month)
        .where(Customer.created_at <= month_begin)
    )
    previous_month_count = db.session.scalar(query)
    stats["new_customers_percent"] = (
        0
        if stats["new_customers"] == 0
        else (stats["new_customers"] - previous_month_count)
        / stats["new_customers"]
        * 100
    )

    stats["revenue"] = db.session.scalar(query)  # todo
    stats["revenue_percent"] = db.session.scalar(query)  # todo
    return render_template("admin/index.html", stats=stats)


admin_bp.register_blueprint(auth_bp)
admin_bp.register_blueprint(books_bp)
admin_bp.register_blueprint(orders_bp)
admin_bp.register_blueprint(shopping_bp)
admin_bp.register_blueprint(withdraw_bp)
admin_bp.register_blueprint(location_bp)


@admin_bp.before_request
def before_request():
    if not logged_in() and request.path not in [url_for("admin.auth.login")]:
        path = request.path
        return redirect(url_for("admin.auth.login", next=path))
