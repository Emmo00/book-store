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

from app import db
from app.forms import AdminLocationForm
from app.helpers.image import save_file
from app.models import PickupLocation, LocationImage


location_bp = Blueprint("locations", __name__, url_prefix="/locations")


@location_bp.route("/")
def locations():
    locations = db.session.scalars(
        sa.select(PickupLocation).order_by(PickupLocation.name.asc())
    )
    return render_template(
        "admin/locations.html", title="Locations", locations=locations
    )


@location_bp.route("/<location_id>", methods=["GET", "POST"])
def location(location_id):
    location: PickupLocation = db.first_or_404(
        sa.select(PickupLocation).where(PickupLocation.id == location_id)
    )
    form = AdminLocationForm(location.name)
    if form.validate_on_submit():
        files = request.files.getlist("images")
        if len(files) > 0 and files[0].filename != "":
            images = db.session.scalars(
                sa.select(LocationImage).where(LocationImage.location_id == location.id)
            )
            # delete previously existing images
            for image in images:
                try:
                    os.remove(f"{current_app.config['UPLOADS_FOLDER']}/{image.name}")
                    db.session.delete(image)
                except:
                    print("could not delete", image.path)
            # save new images
            for file in files:
                saved_file = save_file(file, LocationImage)
                saved_file.location_id = location.id
                db.session.add(saved_file)
        if form.name.data != location.name:
            location.name = form.name.data
        if form.description.data != location.description:
            location.description = form.description.data
        db.session.add(location)
        db.session.commit()
        flash("Location Updated")
        return redirect(url_for("admin.locations.location", location_id=location.id))
    form.name.data = location.name
    form.description.data = location.description
    return render_template(
        "admin/location_preview.html", title=location.name, location=location, form=form
    )


@location_bp.route("/new", methods=["GET", "POST"])
def add_location():
    form = AdminLocationForm("")
    location = PickupLocation()
    images = []
    if form.validate_on_submit():
        files = request.files.getlist("images")
        if len(files) >= 0 and files[0].filename != "":
            for file in files:
                saved_file = save_file(file, LocationImage)
                images.append(saved_file)
        location.name = form.name.data
        location.description = form.description.data
        db.session.add(location)
        db.session.commit()
        for image in images:
            image.location_id = location.id
        db.session.add_all(images)
        db.session.commit()
        flash("Location Saved")
        return redirect(url_for("admin.locations.add_location"))
    return render_template(
        "admin/location_preview.html",
        title="New Location",
        form=form,
        location=location,
    )
