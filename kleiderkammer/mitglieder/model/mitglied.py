from kleiderkammer.util.db import db


class Mitglied(db.Model):
    __tablename__ = 'mitglied'
    id = db.Column(db.BigInteger, primary_key=True)
    vorname = db.Column(db.VARCHAR(255), nullable=False)
    nachname = db.Column(db.VARCHAR(255), nullable=False)
    pictureURL = db.Column(db.VARCHAR(255), nullable=True)
    aktiv = db.Column(db.Boolean, default=True)

    db.UniqueConstraint(vorname, nachname)
