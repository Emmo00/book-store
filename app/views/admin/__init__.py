from flask import Blueprint, render_template


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@admin_bp.route("/home")
@admin_bp.route("/dashboard")
def index():
    return render_template("admin/index.html")
