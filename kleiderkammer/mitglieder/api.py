from flask import Blueprint, request, Response

from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.db import db
from kleiderkammer.util.oidc import oidc

api = Blueprint('mitglieder_api', __name__)


@api.route("/add", methods=["POST"])
@oidc.require_login
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
