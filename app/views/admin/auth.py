from urllib.parse import urlsplit

from flask import (
    Blueprint,
    render_template,
    session,
    current_app,
    redirect,
    url_for,
    flash,
    request,
)

from app.forms import AdminLoginForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def logged_in():
    if not session.get("ADMIN_USER") or not session.get("ADMIN_PASS"):
        return False
    username = session.get("ADMIN_USER")
    password = session.get("ADMIN_PASS")
    if (
        username != current_app.config["ADMIN_USER"]
        or password != current_app.config["ADMIN_PASS"]
    ):
        return False
    return True


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if logged_in():
        return redirect(url_for("admin.index"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if (
            username != current_app.config["ADMIN_USER"]
            or password != current_app.config["ADMIN_PASS"]
        ):
            flash("Invalid username or password")
            return redirect(url_for("admin.auth.login"))
        session["ADMIN_USER"] = username
        session["ADMIN_PASS"] = password
        flash("Login Successful")
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("admin.index")
        return redirect(next_page)
    return render_template("admin/login.html", title="Login", form=form)


@auth_bp.route("/logout")
def logout():
    session.pop("ADMIN_USER")
    session.pop("ADMIN_PASS")
    return redirect(url_for("admin.auth.login"))
