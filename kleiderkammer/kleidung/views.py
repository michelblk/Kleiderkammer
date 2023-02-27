from operator import and_

import flask_login
from flask import Blueprint, render_template
from sqlalchemy import case
from sqlalchemy.sql.functions import coalesce, count

from kleiderkammer.kleidung.model.kleidung import Kleidung
from kleiderkammer.kleidung.model.kleidungskategorie import Kleidungskategorie
from kleiderkammer.kleidung.model.kleidungsleihe import Kleidungsleihe
from kleiderkammer.kleidung.model.kleidungstyp import Kleidungstyp
from kleiderkammer.kleidung.model.kleidungswaesche import Kleidungswaesche
from kleiderkammer.mitglieder.model.mitglied import Mitglied

kleidung = Blueprint("kleidung", __name__, template_folder="templates")


@kleidung.route("/", methods=["GET"])
@flask_login.login_required
def index():
    rows = (
        Kleidung.query.filter_by(archiviert=False)
        .join(
            Kleidungswaesche, Kleidung.id == Kleidungswaesche.kleidung_id, isouter=True
        )
        .join(Kleidungstyp, Kleidung.typ_id == Kleidungstyp.id, isouter=True)
        .join(
            Kleidungskategorie,
            Kleidungstyp.kategorie_id == Kleidungskategorie.id,
            isouter=True,
        )
        .join(
            Kleidungsleihe,
            and_(Kleidungsleihe.bis == None, Kleidung.id == Kleidungsleihe.kleidung_id),
            isouter=True,
        )
        .join(Mitglied, Mitglied.id == Kleidungsleihe.mitglied_id, isouter=True)
        .with_entities(
            Kleidung.id,
            Kleidung.typ_id,
            Kleidungskategorie.id.label("kategorie_id"),
            Kleidung.code,
            Kleidungskategorie.name.label("kategorie_name"),
            Kleidungstyp.hersteller.label("typ_hersteller"),
            Kleidungstyp.modell.label("typ_modell"),
            Kleidung.groesse,
            Kleidung.anschaffungsjahr,
            coalesce(count(Kleidungswaesche.kleidung_id), 0).label("waeschen"),
            case(
                [
                    (
                        coalesce(count(Kleidungswaesche.von), 0)
                        == coalesce(count(Kleidungswaesche.bis), 0),
                        False,
                    )
                ],
                else_=True,
            ).label("in_waesche"),
            case(
                [
                    (
                        Kleidungsleihe.mitglied_id != None,
                        Mitglied.nachname + ", " + Mitglied.vorname,
                    )
                ],
                else_=None,
            ).label("ausgeliehen_an"),
        )
        .group_by(Kleidung)
        .order_by(Kleidung.code)
        .all()
    )

    kategorien = Kleidungskategorie.query.order_by(Kleidungskategorie.name).all()
    kategorien = [kleidungskategorie.name for kleidungskategorie in kategorien]

    hersteller = (
        Kleidungstyp.query.with_entities(Kleidungstyp.hersteller)
        .distinct()
        .order_by(Kleidungstyp.hersteller)
        .all()
    )
    hersteller = [kleidungstyp.hersteller for kleidungstyp in hersteller]

    modelle = (
        Kleidungstyp.query.with_entities(Kleidungstyp.modell)
        .distinct()
        .order_by(Kleidungstyp.modell)
        .all()
    )
    modelle = [kleidungstyp.modell for kleidungstyp in modelle]

    groessen = (
        Kleidung.query.with_entities(Kleidung.groesse)
        .distinct()
        .order_by(Kleidung.groesse)
        .all()
    )
    groessen = [kleidung.groesse for kleidung in groessen]

    jahre = (
        Kleidung.query.with_entities(Kleidung.anschaffungsjahr)
        .distinct()
        .order_by(Kleidung.anschaffungsjahr)
        .all()
    )
    jahre = [kleidung.anschaffungsjahr for kleidung in jahre]

    waeschen = (
        Kleidungswaesche.query.with_entities(
            coalesce(count(Kleidungswaesche.kleidung_id), 0).label("waeschen")
        )
        .group_by(Kleidungswaesche.kleidung_id)
        .distinct()
        .order_by("waeschen")
        .all()
    )
    waeschen = [waesche.waeschen for waesche in waeschen]

    return render_template(
        "html/kleidung.html",
        rows=rows,
        kategorien=kategorien,
        hersteller=hersteller,
        modelle=modelle,
        groessen=groessen,
        jahre=jahre,
        waeschen=waeschen,
    )


@kleidung.route("/hinzufuegen", methods=["GET"])
@flask_login.login_required
def hinzufuegen():
    modelle = Kleidungstyp.query.order_by(
        Kleidungstyp.kategorie_id, Kleidungstyp.modell, Kleidungstyp.hersteller
    ).all()

    groessen = (
        Kleidung.query.with_entities(Kleidung.groesse)
        .distinct()
        .order_by(Kleidung.groesse)
        .all()
    )
    groessen = [r.groesse for r in groessen]

    return render_template(
        "html/kleidung-hinzufuegen.html", modelle=modelle, groessen=groessen
    )
