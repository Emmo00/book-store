from flask import Blueprint
from .books import books_bp
from .orders import orders_bp


api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(books_bp)
api_bp.register_blueprint(orders_bp)
