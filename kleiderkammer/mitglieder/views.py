from flask import Blueprint, render_template

from kleiderkammer.util.oidc import oidc

mitglieder = Blueprint('mitglieder', __name__, template_folder="templates")


@mitglieder.route("/")
@oidc.require_login
def index():
    return render_template("mitglieder.html")
