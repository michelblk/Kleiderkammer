import flask_login
from flask import Blueprint, render_template

einstellungen = Blueprint('einstellungen', __name__, template_folder="templates")


@einstellungen.route("/")
@flask_login.login_required
def index():
    return render_template("html/einstellungen.html")
