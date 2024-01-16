from uuid import uuid4

from flask import Blueprint, jsonify, request, session
import sqlalchemy as sa

from app import db
from app.models import Order, Customer, BookOrder, Book
from app.helpers.payment import create_payment

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/", methods=["POST"])
def create_order():
    # GET REQUEST PAYLOAD
    payload = request.json
    if (
        not payload.get("name")
        or not payload.get("email")
        or not payload.get("phone")
        or not payload.get("books")
        or not payload.get("location")
        or payload.get("location") == "default"
    ):
        return jsonify({"message": "Incomplete information"}), 400
    # CREATE CUSTOMER
    customer_id = session.get("user_id") or str(uuid4())
    customer = Customer(
        id=customer_id,
        name=payload.get("name"),
        phone=payload.get("phone"),
        email=payload.get("email"),
    )
    db.session.add(customer)
    # CREATE ORDER
    order_id = str(uuid4())
    order = Order(
        id=order_id, customer_id=customer_id, pickup_location_id=payload.get("location")
    )
    db.session.add(order)
    # CREATE BOOKORDERS
    book_orders = []
    total = 0
    for book_id in payload.get("books"):
        book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
        if book:
            book_order = BookOrder(
                book_id=book_id,
                order_id=order_id,
                quantity=payload.get("books").get(book_id),
            )
            book_orders.append(book_order)
            total += book.selling_price * int(payload.get("books").get(book_id))
    db.session.add_all(book_orders)
    # CREATE FLUTTERWAVE PAYMENT
    payment = create_payment(
        order_id, total, customer_id, customer.name, customer.email, customer.phone
    )
    # RETURN FLUTTERWAVE PAYMENT URL
    if payment:
        session["user_id"] = customer_id
        return jsonify(payment)
    return jsonify({"message": "Error creating payment"}), 500


@orders_bp.route("/webhook-callback", methods=["POST"])
def webhook_callback():
    # CONFIRM ORDER
    # UPDATE ORDER
    pass
