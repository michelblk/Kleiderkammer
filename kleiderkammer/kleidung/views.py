from flask import Blueprint, render_template

from kleiderkammer.kleidung.model.kleidung import Kleidung
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

    return render_template("html/kleidung.html", rows=rows)


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
