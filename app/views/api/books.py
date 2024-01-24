from flask import jsonify, Blueprint
import sqlalchemy as sa
from app import db
from app.models import Book


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/<bookId>", strict_slashes=False)
def book(bookId):
    book = db.session.scalar(sa.select(Book).where(Book.id == bookId))
    if not book:
        print("here")
        return jsonify({"message": "Not Found", "data": {}}), 404
    return jsonify(
        {
            "message": "Book info",
            "data": {"id": bookId, "title": book.title, "price": book.selling_price},
        }
    )
