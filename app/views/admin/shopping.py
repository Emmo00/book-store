from flask import Blueprint, render_template
import sqlalchemy as sa

from app import db
from app.models import Shopping

shopping_bp = Blueprint("shopping", __name__, url_prefix="/shopping")


@shopping_bp.route("/")
def shopping():
    shopping = db.session.scalars(sa.select(Shopping))
    return render_template(
        "admin/shopping.html", title="Shopping List", shopping=shopping
    )
