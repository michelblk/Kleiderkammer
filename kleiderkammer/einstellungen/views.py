from flask import Blueprint, render_template

from kleiderkammer.util.oidc import oidc

einstellungen = Blueprint('einstellungen', __name__, template_folder="templates")


@einstellungen.route("/")
@oidc.require_login
def index():
    return render_template("einstellungen.html")
