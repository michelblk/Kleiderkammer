import flask_login
from flask import Blueprint, Response, request
from werkzeug.security import check_password_hash

from kleiderkammer.login.model.User import User
from kleiderkammer.util.db import db

api = Blueprint('einstellungen_api', __name__)


@api.route("/user", methods=["PUT"])
@flask_login.login_required
def add_user():
    data = request.form

    username = data["username"]
    password = data["password"]

    if username and password:
        user = User()
        user.username = username
        user.password = password
        user.hasToChangePassword = True

        db.session.add(user)

        try:
            db.session.commit()
            return Response(status=201)
        except Exception:
            return Response(status=400)


@api.route("/password", methods=["POST"])
@flask_login.login_required
def change_password():
    data = request.form

    current_password = data["current-password"]
    new_password = data["new-password"]
    new_password2 = data["new-password2"]

    user = User.query \
        .filter_by(username=flask_login.current_user.username) \
        .one_or_none()

    if current_password and new_password and new_password2 and new_password == new_password2 \
            and check_password_hash(user.password, current_password):
        user.password = new_password

        db.session.add(user)
        db.session.commit()
