from flask import Blueprint, render_template
import sqlalchemy as sa

from app import db
from app.models import PickupLocation


cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/", strict_slashes=False)
def preview():
    return render_template("cart_preview.html")


@cart_bp.route("/form", strict_slashes=False)
def form():
    locations = db.session.scalars(sa.select(PickupLocation))
    return render_template("cart_form.html", locations=locations)
