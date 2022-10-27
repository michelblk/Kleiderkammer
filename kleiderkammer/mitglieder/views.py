from flask import Blueprint, render_template

from kleiderkammer.kleidung.model.kleidungsleihe import Kleidungsleihe
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

    Mitglied.query.join(Kleidungsleihe).all()  # FIXME

    return render_template("html/mitglieder.html", rows=rows)


@mitglieder.route("/hinzufuegen", methods=["GET"])
@oidc.require_login
def hinzufuegen():
    return render_template("html/mitglied-hinzufuegen.html")
