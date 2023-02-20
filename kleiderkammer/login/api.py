import flask_login
from flask import Blueprint, redirect, request, session, url_for
from werkzeug.security import check_password_hash

from kleiderkammer.login.model.User import User

api = Blueprint("login_api", __name__)


@api.route("/", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).one_or_none()

    if user and check_password_hash(user.password, password):
        flask_login.login_user(user)
        session["id"] = user.id

        if user.hasToChangePassword:
            return redirect(url_for("einstellungen.index"))
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("login.index"))


@api.route("/logout", methods=["GET"])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    session["id"] = None
    return redirect(url_for("login.index"))
