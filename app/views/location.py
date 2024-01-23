from flask import render_template, Blueprint
import sqlalchemy as sa

from app import db
from app.models import PickupLocation


location_bp = Blueprint("locations", __name__, url_prefix="/locations")


@location_bp.route("/", strict_slashes=False)
def locations():
    locations = db.session.scalars(sa.select(PickupLocation))
    return render_template("locations.html", locations=locations)


@location_bp.route("/<location_id>", strict_slashes=False)
def location(location_id):
    location = db.first_or_404(
        sa.select(PickupLocation).where(PickupLocation.id == location_id)
    )
    return render_template("location_preview.html", location=location)
