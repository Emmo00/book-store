import requests

from flask import current_app
import sqlalchemy as sa

from app import db
from app.models import Order
from .order_status import OrderStatus


def create_payment(
    txn_ref, amount, customer_id, customer_name, customer_email, customer_phone
):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {"Authorization": f"Bearer {current_app.config['FLW_SECRET_KEY']}"}
    data = {
        "tx_ref": txn_ref,
        "amount": float(amount),
        "currency": "NGN",
        "redirect_url": f"{current_app.config['APP_URL']}/payment-complete",
        "meta": {
            "consumer_id": customer_id,
        },
        "customer": {
            "email": customer_email,
            "phonenumber": customer_phone,
            "name": customer_name,
        },
        "customizations": {"title": current_app.config["APP_NAME"], "logo": ""},
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except requests.exceptions.RequestException as err:
        print(err)
        return {}


def confirm_transaction(order_id):
    headers = {
        "Authorization": f"Bearer {current_app.config['FLW_SECRET_KEY']}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(
            f"https://api.flutterwave.com/v3/transactions/{order_id}/verify",
            headers=headers,
        )
        if response.json().get("status") == "success":
            return True
        return False
    except requests.exceptions.RequestException as err:
        print(err)
        return False


def update_order(order_id, status=OrderStatus.sent):
    order = db.session.scalar(sa.select(Order).where(Order.id == order_id))
    if not order:
        return
    order.status = status
    db.session.add(order)
    db.session.commit()
