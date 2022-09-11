from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from kleiderkammer.einstellungen.api import api as einstellungen_api
from kleiderkammer.einstellungen.views import einstellungen
from kleiderkammer.kleidung.views import kleidung
from kleiderkammer.mitglieder.views import mitglieder
from kleiderkammer.util import db
from kleiderkammer.util.oidc import oidc


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(kleidung, url_prefix='/kleidung')
    app.register_blueprint(mitglieder, url_prefix='/mitglieder')
    app.register_blueprint(einstellungen, url_prefix='/einstellungen')
    app.register_blueprint(einstellungen_api, url_prefix='/api/einstellungen')

    # initialize oidc client
    oidc.init_app(app)

    # initialize database
    db.init_app(app)

    @app.context_processor
    def inject_userinfo():
        info = oidc.user_getinfo(['name'])
        return {'username': info['name']}

    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}

    return app


if __name__ == '__main__':
    create_app().run()
