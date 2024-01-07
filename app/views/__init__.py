from flask import Blueprint, render_template

client_bp = Blueprint("client", __name__)


@client_bp.route("/")
@client_bp.route("/home")
def index():
    return render_template("index.html")
