from flask import Blueprint, render_template
from sqlalchemy.sql.functions import count, coalesce

from kleiderkammer.kleidung.model.kleidungsleihe import Kleidungsleihe
from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.oidc import oidc

mitglieder = Blueprint('mitglieder', __name__, template_folder="templates")


@mitglieder.route("/")
@oidc.require_login
def index():
    ausgeliehene_kleidung = Kleidungsleihe.query \
        .with_entities(Kleidungsleihe.mitglied_id, count(Kleidungsleihe.kleidung_id).label("count")) \
        .filter(Kleidungsleihe.bis == None) \
        .subquery()

    rows = Mitglied.query \
        .filter_by(aktiv=True) \
        .join(Kleidungsleihe, Mitglied.id == Kleidungsleihe.mitglied_id, isouter=True) \
        .join(ausgeliehene_kleidung, Mitglied.id == ausgeliehene_kleidung.c.mitglied_id, isouter=True) \
        .with_entities(Mitglied.id, Mitglied.nachname, Mitglied.vorname,
                       # Anzahl der aktuell ausgeliehene Kleidung
                       coalesce(ausgeliehene_kleidung.c.count, 0).label("ausgeliehene_kleidung_count")
                       ) \
        .group_by(Mitglied) \
        .order_by(Mitglied.nachname, Mitglied.vorname) \
        .all()

    return render_template("html/mitglieder.html", rows=rows)


@mitglieder.route("/hinzufuegen", methods=["GET"])
@oidc.require_login
def hinzufuegen():
    return render_template("html/mitglied-hinzufuegen.html")
