from flask import Blueprint, render_template

from kleiderkammer.kleidung.model.kleidung import Kleidung
from kleiderkammer.kleidung.model.kleidungskategorie import Kleidungskategorie
from kleiderkammer.kleidung.model.kleidungstyp import Kleidungstyp
from kleiderkammer.util.oidc import oidc

kleidung = Blueprint('kleidung', __name__, template_folder="templates")


@kleidung.route("/", methods=['GET'])
@oidc.require_login
def index():
    rows = Kleidung.query \
        .filter_by(archiviert=False) \
        .order_by(Kleidung.code) \
        .all()

    kategorien = Kleidungskategorie.query \
        .order_by(Kleidungskategorie.name) \
        .all()
    kategorien = [kleidungskategorie.name for kleidungskategorie in kategorien]

    hersteller = Kleidungstyp.query \
        .with_entities(Kleidungstyp.hersteller) \
        .distinct() \
        .order_by(Kleidungstyp.hersteller) \
        .all()
    hersteller = [kleidungstyp.hersteller for kleidungstyp in hersteller]

    modelle = Kleidungstyp.query \
        .with_entities(Kleidungstyp.modell) \
        .distinct() \
        .order_by(Kleidungstyp.modell) \
        .all()
    modelle = [kleidungstyp.modell for kleidungstyp in modelle]

    groessen = Kleidung.query \
        .with_entities(Kleidung.groesse) \
        .distinct() \
        .order_by(Kleidung.groesse) \
        .all()
    groessen = [kleidung.groesse for kleidung in groessen]

    jahre = Kleidung.query \
        .with_entities(Kleidung.anschaffungsjahr) \
        .distinct() \
        .order_by(Kleidung.anschaffungsjahr) \
        .all()
    jahre = [kleidung.anschaffungsjahr for kleidung in jahre]

    waeschen = []

    return render_template("html/kleidung.html", rows=rows, kategorien=kategorien, hersteller=hersteller,
                           modelle=modelle, groessen=groessen, jahre=jahre, waeschen=waeschen)


@kleidung.route("/hinzufuegen", methods=["GET"])
@oidc.require_login
def hinzufuegen():
    modelle = Kleidungstyp.query \
        .all()

    groessen = Kleidung.query \
        .with_entities(Kleidung.groesse) \
        .distinct() \
        .all()
    groessen = [r.groesse for r in groessen]

    return render_template("html/kleidung-hinzufuegen.html", modelle=modelle, groessen=groessen)
