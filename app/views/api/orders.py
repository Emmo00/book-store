from flask import Blueprint, jsonify, request
import sqlalchemy as sa

from app import db
from app.models import Order

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/", methods=["POST"])
def create_order():
    pass
