from datetime import datetime

import flask_login
from flask import Blueprint, Response, request
from sqlalchemy.exc import NoResultFound

from kleiderkammer.kleidung.model.kleidung import Kleidung
from kleiderkammer.kleidung.model.kleidungskategorie import Kleidungskategorie
from kleiderkammer.kleidung.model.kleidungsleihe import Kleidungsleihe
from kleiderkammer.kleidung.model.kleidungstyp import Kleidungstyp
from kleiderkammer.kleidung.model.kleidungswaesche import Kleidungswaesche
from kleiderkammer.mitglieder.model.mitglied import Mitglied
from kleiderkammer.util.db import db

api = Blueprint("kleidung_api", __name__)


@api.route("/hinzufuegen", methods=["POST"])
@flask_login.login_required
def hinzufuegen():
    data = request.form

    modell = data["modell"]
    hersteller = data["hersteller"]
    kategoriename = data["kategorie"]
    code = data["code"]
    groesse = data["groesse"]
    anschaffungsjahr = data["anschaffungsjahr"]

    if (
        modell
        and hersteller
        and kategoriename
        and code
        and groesse
        and anschaffungsjahr
    ):
        # get kategorie id
        try:
            kategorie = Kleidungskategorie.query.filter_by(name=kategoriename).one()
        except NoResultFound:
            kategorie = Kleidungskategorie()
            kategorie.name = kategoriename

            db.session.add(kategorie)
            db.session.flush()
            db.session.refresh(kategorie)

        # get typ id
        try:
            typ = Kleidungstyp.query.filter_by(
                hersteller=hersteller, modell=modell, kategorie_id=kategorie.id
            ).one()
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


@api.route("/<kleidung_id>", methods=["DELETE"])
@flask_login.login_required
def archivieren(kleidung_id):
    kleidung = Kleidung.query.filter_by(id=kleidung_id).first()
    kleidung.archiviert = True
    db.session.add(kleidung)

    aktive_waesche = Kleidungswaesche.query.filter_by(
        kleidung_id=kleidung_id, bis=None
    ).one_or_none()
    if aktive_waesche:
        aktive_waesche.bis = datetime.now()
        db.session.add(aktive_waesche)

    aktive_leihe = Kleidungsleihe.query.filter_by(
        kleidung_id=kleidung_id, bis=None
    ).one_or_none()
    if aktive_leihe:
        aktive_leihe.bis = datetime.now()
        db.session.add(aktive_leihe)

    db.session.commit()
    return Response(status=204)


@api.route("/toggle_waesche", methods=["POST"])
@flask_login.login_required
def toggle_waesche():
    data = request.form
    kleidung_id = data["kleidung_id"]
    action = data["action"]

    waesche = Kleidungswaesche.query.filter_by(
        kleidung_id=kleidung_id, bis=None
    ).scalar()

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


@api.route("/status", methods=["GET"])
@flask_login.login_required
def status():
    kleidung_id = request.args["kleidungId"]

    kleidung = Kleidung.query.filter_by(id=kleidung_id).first()

    letzte_waesche = (
        Kleidungswaesche.query.filter_by(kleidung_id=kleidung_id)
        .order_by(Kleidungswaesche.von.desc())
        .first()
    )

    aktuelle_leihe = (
        Kleidungsleihe.query.filter_by(kleidung_id=kleidung_id, bis=None)
        .join(Mitglied, Kleidungsleihe.mitglied_id == Mitglied.id, isouter=True)
        .with_entities(Kleidungsleihe.von, Mitglied.vorname, Mitglied.nachname)
        .order_by(Kleidungsleihe.von)
        .one_or_none()
    )

    response = {
        "archiviert": kleidung.archiviert,
        "isInWaesche": letzte_waesche.bis is None if letzte_waesche else False,
        "zuletztGewaschen": letzte_waesche.von if letzte_waesche else None,
        "leihe": {
            "mitglied": {
                "vorname": aktuelle_leihe.vorname if aktuelle_leihe else None,
                "nachname": aktuelle_leihe.nachname if aktuelle_leihe else None,
            }
            if aktuelle_leihe
            else None,
            "seit": aktuelle_leihe.von if aktuelle_leihe else None,
        },
    }

    return response


@api.route("/<kleidung_id>/leihen", methods=["GET"])
@flask_login.login_required
def leihen(kleidung_id):
    leihen = (
        Kleidungsleihe.query.filter_by(kleidung_id=kleidung_id)
        .join(Mitglied, Kleidungsleihe.mitglied_id == Mitglied.id, isouter=True)
        .with_entities(
            Kleidungsleihe.von,
            Kleidungsleihe.bis,
            Mitglied.id.label("mitglied_id"),
            Mitglied.vorname,
            Mitglied.nachname,
        )
        .order_by(Kleidungsleihe.von.desc())
        .all()
    )

    return [
        {
            "mitglied": {
                "id": leihe.mitglied_id,
                "vorname": leihe.vorname,
                "nachname": leihe.nachname,
            },
            "von": leihe.von,
            "bis": leihe.bis,
        }
        for leihe in leihen
    ]


@api.route("/<kleidung_id>/waeschen", methods=["GET"])
@flask_login.login_required
def waeschen(kleidung_id):
    waeschen = (
        Kleidungswaesche.query.filter_by(kleidung_id=kleidung_id)
        .order_by(Kleidungswaesche.von.desc())
        .all()
    )

    return [{"von": waesche.von, "bis": waesche.bis} for waesche in waeschen]


@api.route("/verleihen", methods=["POST"])
@flask_login.login_required
def verleihen():
    mitglied_id = request.form["mitgliedId"]
    kleidung_id = request.form["kleidungId"]

    leihe = Kleidungsleihe()
    leihe.von = datetime.now()
    leihe.kleidung_id = kleidung_id
    leihe.mitglied_id = mitglied_id

    db.session.add(leihe)
    db.session.commit()

    return Response(status=201)


@api.route("/verleihen", methods=["DELETE"])
@flask_login.login_required
def zuruecknehmen():
    kleidung_id = request.form["kleidungId"]

    leihe = Kleidungsleihe.query.filter_by(kleidung_id=kleidung_id, bis=None).one()

    leihe.bis = datetime.now()

    db.session.add(leihe)
    db.session.commit()

    return Response(status=201)
