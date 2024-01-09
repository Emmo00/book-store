from flask import Blueprint, render_template
import sqlalchemy as sa

from app.models import Book
from app import db


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/<book_id>", strict_slashes=False)
@books_bp.route("/<book_id>/<book_slug>", strict_slashes=False)
def book(book_id, book_slug=""):
    book = db.first_or_404(sa.select(Book).where(Book.id == book_id))
    return render_template("book_preview.html", book=book, title=book.title)
