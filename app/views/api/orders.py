from uuid import uuid4

from flask import Blueprint, jsonify, request, session
import sqlalchemy as sa

from app import db
from app.models import Order, Customer, BookOrder, Book
from app.helpers.payment import create_payment

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/", methods=["POST"], strict_slashes=False)
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
    customer_id = session.get("user_id")
    customer = db.session.scalar(sa.select(Customer).where(Customer.id == customer_id))
    if not customer:
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
    order.total = total
    db.session.add(order)
    db.session.add_all(book_orders)
    db.session.commit()
    # CREATE FLUTTERWAVE PAYMENT
    payment = create_payment(
        order_id, total, customer_id, customer.name, customer.email, customer.phone
    )
    # RETURN FLUTTERWAVE PAYMENT URL
    if payment:
        return jsonify(payment)
    return jsonify({"message": "Error creating payment"}), 500
