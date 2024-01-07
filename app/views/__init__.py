from uuid import uuid4

from flask import Blueprint, render_template, current_app, session

from .books import books_bp
from .cart import cart_bp
from .order import orders_bp

client_bp = Blueprint("client", __name__)


@client_bp.route("/", strict_slashes=False)
@client_bp.route("/home")
def index():
    return render_template("index.html")


client_bp.register_blueprint(books_bp)
client_bp.register_blueprint(cart_bp)
client_bp.register_blueprint(orders_bp)


@client_bp.before_request
def before_request():
    if not session["user_id"]:
        session.user_id = str(uuid4())
