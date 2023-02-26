from kleiderkammer.util.db import db


class Kleidungskategorie(db.Model):
    __tablename__ = "kleidungskategorie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(50))
