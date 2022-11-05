from sqlalchemy.ext.declarative import DeferredReflection
from sqlalchemy.orm import declarative_base

from kleiderkammer.util.db import db

Base = declarative_base(cls=DeferredReflection)


class Kleidungsleihe(db.Model):
    __tablename__ = 'kleidungsleihe'
    id = db.Column(db.BigInteger, primary_key=True)
    mitglied_id = db.Column(db.BigInteger, db.ForeignKey('mitglied.id'))
    kleidung_id = db.Column(db.BigInteger, db.ForeignKey('kleidung.id'))
    von = db.Column(db.DateTime, nullable=False)
    bis = db.Column(db.DateTime, nullable=True)
