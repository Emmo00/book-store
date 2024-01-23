from flask import Blueprint, render_template, current_app
import sqlalchemy as sa

from app import db
from app.forms import AdminWithdrawForm
from app.helpers.payment import cashout
from app.models import Shopping

withdraw_bp = Blueprint("withdraw", __name__, url_prefix="/withdraw")


@withdraw_bp.route("/", methods=["GET", "POST"])
def withdraw():
    form = AdminWithdrawForm()
    if form.validate_on_submit():
        pass
    shopping = db.session.scalars(sa.select(Shopping))
    shopping_total = 0
    for item in shopping:
        shopping_total += item.quantity * item.book.original_price
    form.amount.data = shopping_total

    return render_template("admin/withdraw.html", title="Withdraw", form=form)
