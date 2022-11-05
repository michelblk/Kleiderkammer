import flask_login

from kleiderkammer.util.db import db


class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(50), index=True, unique=True, nullable=False)
    password = db.Column(db.VARCHAR(150), nullable=False)
