from kleiderkammer.util.db import db


class Kleidungskategorie(db.Model):
    __tablename__ = 'kleidungskategorie'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.VARCHAR(50))
    empfohlen = db.Column(db.Boolean)
