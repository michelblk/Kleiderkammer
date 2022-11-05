from kleiderkammer.kleidung.model.kleidungstyp import Kleidungstyp
from kleiderkammer.util.db import db


class Kleidung(db.Model):
    __tablename__ = 'kleidung'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.VARCHAR(50), index=True, unique=True, nullable=False)
    typ_id = db.Column(db.BigInteger, db.ForeignKey("kleidungstyp.id"), nullable=False)
    typ = db.relationship("Kleidungstyp", backref=db.backref("kleidungstyp", uselist=False))
    groesse = db.Column(db.VARCHAR(10))
    anschaffungsjahr = db.Column(db.Integer, nullable=False)
    archiviert = db.Column(db.Boolean)
