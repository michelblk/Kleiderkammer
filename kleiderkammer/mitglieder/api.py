from datetime import datetime

import flask_login
from flask import Blueprint, Response, request

from kleiderkammer.kleidung.model.kleidungsleihe import Kleidungsleihe
from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.db import db

api = Blueprint("mitglieder_api", __name__)


@api.route("/", methods=["GET"])
@flask_login.login_required
def get():
    mitglieder = (
        Mitglied.query.with_entities(Mitglied.id, Mitglied.vorname, Mitglied.nachname)
        .filter_by(aktiv=True)
        .order_by(Mitglied.nachname, Mitglied.vorname)
        .all()
    )

    response = [
        {"id": mitglied.id, "vorname": mitglied.vorname, "nachname": mitglied.nachname}
        for mitglied in mitglieder
    ]

    return response


@api.route("/add", methods=["POST"])
@flask_login.login_required
def hinzufuegen():
    data = request.form
    if data["nachname"] and data["vorname"]:
        mitglied = Mitglied()
        mitglied.nachname = data["nachname"]
        mitglied.vorname = data["vorname"]

        db.session.add(mitglied)
        db.session.commit()

        return Response(status=201)
    else:
        return Response(status=400)


@api.route("/<mitglied_id>", methods=["DELETE"])
@flask_login.login_required
def entfernen(mitglied_id):
    mitglied = Mitglied.query.filter_by(id=mitglied_id).first()
    mitglied.aktiv = False
    db.session.add(mitglied)

    aktive_leihe = Kleidungsleihe.query.filter_by(mitglied_id=mitglied_id, bis=None).one_or_none()
    if aktive_leihe:
        aktive_leihe.bis = datetime.now()
        db.session.add(aktive_leihe)

    db.session.commit()
    return Response(status=204)
