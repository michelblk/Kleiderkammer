import flask_login
from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash

from kleiderkammer.login.model.User import User

login = Blueprint('login', __name__, template_folder="templates")


@login.route("/", methods=['GET'])
def index():
    return render_template("html/index.html")


@login.route("/", methods=['POST'])
def login_action():
    username = request.form['username']
    password = request.form['password']

    user = User.query \
        .filter_by(username=username) \
        .one_or_none()

    if user and check_password_hash(user.password, password):
        flask_login.login_user(user)
        session["id"] = user.id
        return redirect(url_for("kleidung.index"))
    else:
        return redirect(url_for("login.index"))
