from kleiderkammer.kleidung.model.kleidungskategorie import Kleidungskategorie
from kleiderkammer.util.db import db


class Kleidungstyp(db.Model):
    __tablename__ = "kleidungstyp"
    id = db.Column(db.Integer, primary_key=True)
    hersteller = db.Column(db.VARCHAR(50))
    modell = db.Column(db.VARCHAR(50))
    kategorie_id = db.Column(db.BigInteger, db.ForeignKey("kleidungskategorie.id"))
    kategorie = db.relationship(
        "Kleidungskategorie", backref=db.backref("kleidungskategorie", uselist=False)
    )
