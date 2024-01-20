import os

from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
import sqlalchemy as sa

from app.models import Book, Image
from app import db
from app.forms import AdminBookForm
from app.helpers.image import save_file

books_bp = Blueprint("books", __name__, url_prefix="books")


@books_bp.route("/")
def books():
    books = db.session.scalars(sa.select(Book).order_by(Book.title.asc()))
    return render_template("admin/books.html", title="Books", books=books)


@books_bp.route("/<book_id>", methods=["GET", "POST"])
def book(book_id):
    book: Book = db.first_or_404(sa.select(Book).where(Book.id == book_id))
    form = AdminBookForm(book.title)
    if form.validate_on_submit():
        files = request.files.getlist("images")
        if len(files) > 0 and files[0].filename != "":
            # delete previously existing images
            images = db.session.scalars(
                sa.select(Image).where(Image.book_id == book.id)
            )
            for image in images:
                try:
                    os.remove(f"{current_app.config['UPLOADS_FOLDER']}/{image.name}")
                    db.session.delete(image)
                except:
                    print("could not delete", image.path)
            # save new files.
            for file in files:
                saved_file = save_file(file, Image)
                saved_file.book_id = book.id
                db.session.add(saved_file)
        if form.title.data != book.title:
            book.title = form.title.data
        if form.description.data != book.description:
            book.description = form.description.data
        if form.original_price.data != str(book.original_price):
            book.original_price = float(form.original_price.data)
        if form.selling_price.data != str(book.selling_price):
            book.selling_price = form.selling_price.data
        db.session.add(book)
        db.session.commit()
        flash("Book Updated")
        return redirect(url_for("admin.books.book", book_id=book.id))
    form.title.data = book.title
    form.description.data = book.description
    form.original_price.data = book.original_price
    form.selling_price.data = book.selling_price
    return render_template(
        "admin/book_preview.html", title=book.title, book=book, form=form
    )


@books_bp.route("/new", methods=["GET", "POST"])
def add_book():
    form = AdminBookForm("")
    book = Book()
    images = []
    if form.validate_on_submit():
        files = request.files.getlist("images")
        if len(files) > 0 and files[0].filename != "":
            for file in files:
                saved_file = save_file(file, Image)
                images.append(saved_file)
        book.title = form.title.data
        book.description = form.description.data
        book.original_price = form.original_price.data
        book.selling_price = form.selling_price.data
        db.session.add(book)
        db.session.commit()
        for image in images:
            image.book_id = book.id
        db.session.add_all(images)
        db.session.commit()
        flash("Book Saved")
        return redirect(url_for("admin.books.add_book"))
    return render_template(
        "admin/book_preview.html", title="New Book", form=form, book=book
    )
