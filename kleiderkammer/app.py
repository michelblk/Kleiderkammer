from datetime import datetime

import flask_login
from flask import Flask, redirect, session
from flask_session import Session

from kleiderkammer.einstellungen.api import api as einstellungen_api
from kleiderkammer.einstellungen.views import einstellungen
from kleiderkammer.kleidung.api import api as kleidung_api
from kleiderkammer.kleidung.views import kleidung
from kleiderkammer.login.model.User import User
from kleiderkammer.login.views import login
from kleiderkammer.mitglieder.api import api as mitglieder_api
from kleiderkammer.mitglieder.views import mitglieder
from kleiderkammer.util import db

print("Starting...")

app = Flask(__name__)
app.config.from_prefixed_env()

# register blueprints
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(kleidung, url_prefix='/kleidung')
app.register_blueprint(kleidung_api, url_prefix='/api/kleidung')
app.register_blueprint(mitglieder, url_prefix='/mitglieder')
app.register_blueprint(mitglieder_api, url_prefix='/api/mitglieder')
app.register_blueprint(einstellungen, url_prefix='/einstellungen')
app.register_blueprint(einstellungen_api, url_prefix='/api/einstellungen')

# initialize database
db.init_app(app)

# initialize session handling
session_management = Session(app)
session_management.app.session_interface.db.create_all()

# initialize login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    return User.query \
        .filter_by(username=username) \
        .one_or_none()


@login_manager.request_loader
def request_loader(request):
    userId = session["id"] if "id" in session else None

    if userId:
        user = User.query \
            .filter_by(id=userId) \
            .one_or_none()
        return user
    return None


@app.context_processor
def inject_userinfo():
    user = flask_login.current_user
    return {'username': user.username if user.is_authenticated else None}


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


@app.route("/")
def index():
    return redirect(app.url_for('login.index'))


if __name__ == '__main__':
    # local testing only. Uwsgi does not call this method
    app.run()
