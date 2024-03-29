from uuid import uuid4

from flask import (
    Blueprint,
    render_template,
    current_app,
    session,
    request,
    url_for,
    abort,
)
import sqlalchemy as sa

from .books import books_bp
from .cart import cart_bp
from .order import orders_bp
from .payment import payment_bp
from .location import location_bp
from app.models import Book
from app import db

client_bp = Blueprint("client", __name__)


@client_bp.route("/", strict_slashes=False, methods=["GET", "POST"])
@client_bp.route("/home")
def index():
    page = request.args.get("page", 1, type=int)
    query = sa.select(Book)
    books = db.paginate(
        query, page=page, per_page=current_app.config["BOOKS_PER_PAGE"], error_out=False
    )
    next_url = url_for("client.index", page=books.next_num) if books.has_next else None
    prev_url = url_for("client.index", page=books.prev_num) if books.has_prev else None

    search_query = request.form.get("search")
    search_results = Book.query.filter(Book.title.ilike(f"%{search_query}%")).all()

    print(session["user_id"])
    return render_template(
        "index.html",
        books=books.items,
        next_url=next_url,
        prev_url=prev_url,
        results=search_results,
    )


client_bp.register_blueprint(books_bp)
client_bp.register_blueprint(cart_bp)
client_bp.register_blueprint(orders_bp)
client_bp.register_blueprint(payment_bp)
client_bp.register_blueprint(location_bp)


@client_bp.before_request
def before_request():
    if not session.get("user_id"):
        print("no session")
        session["user_id"] = str(uuid4())


@client_bp.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404)


@client_bp.errorhandler(500)
def internal_error(e):
    return render_template("error.html", code=500)
