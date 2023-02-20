from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

login = Blueprint("login", __name__, template_folder="templates")


@login.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("app.index"))

    return render_template("html/index.html")
