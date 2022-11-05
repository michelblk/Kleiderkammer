from kleiderkammer.util.db import db


class Kleidungswaesche(db.Model):
    __tablename__ = 'kleidungswaesche'
    id = db.Column(db.Integer, primary_key=True)
    kleidung_id = db.Column(db.BigInteger, db.ForeignKey('kleidung.id'))
    kleidung = db.relationship("Kleidung", backref=db.backref("kleidung", uselist=False))
    von = db.Column(db.DateTime, nullable=False)
    bis = db.Column(db.DateTime, nullable=True)
