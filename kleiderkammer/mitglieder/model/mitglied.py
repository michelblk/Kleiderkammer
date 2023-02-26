from kleiderkammer.util.db import db


class Mitglied(db.Model):
    __tablename__ = "mitglied"
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.VARCHAR(255), nullable=False)
    nachname = db.Column(db.VARCHAR(255), nullable=False)
    aktiv = db.Column(db.Boolean, default=True)

    db.UniqueConstraint(vorname, nachname)
