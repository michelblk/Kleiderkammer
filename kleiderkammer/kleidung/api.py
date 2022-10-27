from datetime import datetime

from flask import Blueprint, Response, request
from sqlalchemy.exc import NoResultFound

from kleiderkammer.kleidung.model.kleidung import Kleidung
from kleiderkammer.kleidung.model.kleidungskategorie import Kleidungskategorie
from kleiderkammer.kleidung.model.kleidungstyp import Kleidungstyp
from kleiderkammer.kleidung.model.kleidungswaesche import Kleidungswaesche
from kleiderkammer.util.db import db
from kleiderkammer.util.oidc import oidc

api = Blueprint('kleidung_api', __name__)


@api.route("/hinzufuegen", methods=["POST"])
@oidc.require_login
def hinzufuegen():
    data = request.form

    modell = data["modell"]
    hersteller = data["hersteller"]
    kategoriename = data["kategorie"]
    code = data["code"]
    groesse = data["groesse"]
    anschaffungsjahr = data["anschaffungsjahr"]

    if modell and hersteller and kategoriename and code and groesse and anschaffungsjahr:
        # get kategorie id
        try:
            kategorie = Kleidungskategorie.query \
                .filter_by(name=kategoriename) \
                .one()
        except NoResultFound:
            kategorie = Kleidungskategorie()
            kategorie.name = kategoriename

            db.session.add(kategorie)
            db.session.flush()
            db.session.refresh(kategorie)

        # get typ id
        try:
            typ = Kleidungstyp.query \
                .filter_by(hersteller=hersteller, modell=modell, kategorie_id=kategorie.id) \
                .one()
        except NoResultFound:
            typ = Kleidungstyp()
            typ.hersteller = hersteller
            typ.modell = modell
            typ.kategorie_id = kategorie.id

            db.session.add(typ)
            db.session.flush()
            db.session.refresh(typ)

        # insert kleidung
        kleidung = Kleidung()
        kleidung.code = code
        kleidung.anschaffungsjahr = anschaffungsjahr
        kleidung.groesse = groesse
        kleidung.archiviert = False
        kleidung.typ_id = typ.id

        db.session.add(kleidung)
        db.session.commit()

    return Response(status=201)


@api.route("/toggle_waesche", methods=["POST"])
@oidc.require_login
def toggle_waesche():
    data = request.form
    kleidung_id = data["kleidung_id"]
    action = data["action"]

    waesche = Kleidungswaesche.query \
        .filter_by(kleidung_id=kleidung_id, bis=None) \
        .scalar()

    erfolg = False
    if action == "abgeben" and not waesche:
        waesche = Kleidungswaesche()
        waesche.kleidung_id = kleidung_id
        waesche.von = datetime.now()
        erfolg = True
    elif action == "erhalten" and waesche:
        waesche.bis = datetime.now()
        erfolg = True

    if erfolg:
        db.session.add(waesche)
        db.session.commit()
        return Response(status=201)

    return Response(status=400)
