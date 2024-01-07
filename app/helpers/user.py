from flask import session
import sqlalchemy as sa

from app import db
from app.models import Customer


def load_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    user = db.session.scalar(sa.select(Customer).where(Customer.id == user_id))
    if not user:
        return None
    return user


current_user = load_user()
