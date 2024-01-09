from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import check_password_hash

from .auth import auth_bp, logged_in
from .books import books_bp
from .orders import orders_bp
from .shopping import shopping_bp
from .withdraw import withdraw_bp


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_bp.route("/home")
@admin_bp.route("/dashboard")
def index():
    return render_template("admin/index.html")


admin_bp.register_blueprint(auth_bp)
admin_bp.register_blueprint(books_bp)
admin_bp.register_blueprint(orders_bp)
admin_bp.register_blueprint(shopping_bp)
admin_bp.register_blueprint(withdraw_bp)


@admin_bp.before_request
def before_request():
    if not logged_in() and request.path not in [url_for("admin.auth.login")]:
        path = request.path
        return redirect(url_for("admin.auth.login", next=path))
