from flask import Blueprint, render_template

from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.oidc import oidc

mitglieder = Blueprint('mitglieder', __name__, template_folder="templates")


@mitglieder.route("/")
@oidc.require_login
def index():
    rows = Mitglied.query \
        .filter_by(aktiv=True) \
        .order_by(Mitglied.nachname, Mitglied.vorname) \
        .all()

    return render_template("mitglieder.html", rows=rows)
