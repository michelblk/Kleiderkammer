import flask_login
from flask import Blueprint, request, Response

from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.db import db

api = Blueprint('mitglieder_api', __name__)


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
