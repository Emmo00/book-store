from flask import Blueprint, render_template


cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/", strict_slashes=False)
def preview():
    return render_template("cart_preview.html")


@cart_bp.route("/form", strict_slashes=False)
def form():
    return render_template("cart_form.html")
