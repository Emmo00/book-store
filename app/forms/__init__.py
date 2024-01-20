from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    TextAreaField,
    SubmitField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Email, ValidationError
import sqlalchemy as sa

from app.models import Book, PickupLocation
from app import db


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AdminBookForm(FlaskForm):
    images = MultipleFileField(
        "Select Book Images", validators=[], render_kw={"multiple": True}
    )

    def __init__(self, original_title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_title = original_title

    title = StringField("Book Title", validators=[DataRequired()])
    description = TextAreaField("Book description", validators=[DataRequired()])
    original_price = StringField("Original Price", validators=[DataRequired()])
    selling_price = StringField("Selling Price", validators=[DataRequired()])
    submit = SubmitField("Save")

    def validate_title(self, title):
        book = db.session.scalar(sa.select(Book).where(Book.title == title.data))
        if book and book.title != self.original_title:
            raise ValidationError("Book with this title already exists")

    def validate_original_price(self, original_price):
        try:
            float(original_price.data)
        except ValueError:
            raise ValidationError("Original Price must be in Number or Decimal format")

    def validate_selling_price(self, selling_price):
        try:
            float(selling_price.data)
        except ValueError:
            raise ValidationError("Selling Price must be in Number or Decimal format")
        if float(selling_price.data) < float(self.original_price.data):
            raise ValidationError("Selling Price must be greater than Original Price")


class AdminLocationForm(FlaskForm):
    images = MultipleFileField(
        "Select Location Images", validators=[], render_kw={"multiple": True}
    )

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    name = StringField("Location Name", validators=[DataRequired()])
    description = TextAreaField("Location description", validators=[DataRequired()])
    submit = SubmitField("Save")

    def validate_name(self, name):
        location = db.session.scalar(
            sa.select(PickupLocation).where(PickupLocation.name == name.data)
        )
        if location and location.name != self.original_name:
            raise ValidationError("Location with this name already exists")
