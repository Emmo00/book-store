from flask import Blueprint, render_template


books_bp = Blueprint("books", __name__, url_prefix="/books")


@books_bp.route("/<book_title>", strict_slashes=False)
def book(book_title):
    return render_template("book_preview.html")
