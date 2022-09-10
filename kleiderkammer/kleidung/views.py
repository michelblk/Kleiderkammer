from flask import Blueprint, render_template

from kleiderkammer.util.oidc import oidc

kleidung = Blueprint('kleidung', __name__, template_folder="templates")


@kleidung.route("/")
@oidc.require_login
def index():
    return render_template("kleidung.html")
