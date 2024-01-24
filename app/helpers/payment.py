import requests

from flask import current_app


def create_payment(
    txn_ref, amount, customer_id, customer_name, customer_email, customer_phone
):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {current_app.config['FLW_SECRET_KEY']}",
        "Content-Type": "application/json",
        "User-Agent": "VeraWeb/1.1",
    }
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
    except Exception as e:
        print(e)
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
        print("verify payment", response.json())
        if response.json().get("status") == "success":
            return True
        return False
    except requests.exceptions.RequestException as err:
        print(err)
        return False


def cashout(amount):
    pass
