from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    TextAreaField,
    SubmitField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, Email, ValidationError


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AdminBookForm(FlaskForm):
    images = MultipleFileField(
        "Select Book Images", validators=[], render_kw={"multiple": True}
    )
    title = StringField("Book Title", validators=[DataRequired()])
    description = TextAreaField("Book description", validators=[DataRequired()])
    original_price = StringField("Original Price", validators=[DataRequired()])
    selling_price = StringField("Selling Price", validators=[DataRequired()])
    submit = SubmitField("Save")

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
