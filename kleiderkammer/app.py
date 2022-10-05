from datetime import datetime

from flask import Flask, redirect

from kleiderkammer.einstellungen.api import api as einstellungen_api
from kleiderkammer.einstellungen.views import einstellungen
from kleiderkammer.kleidung.api import api as kleidung_api
from kleiderkammer.kleidung.views import kleidung
from kleiderkammer.mitglieder.api import api as mitglieder_api
from kleiderkammer.mitglieder.views import mitglieder
from kleiderkammer.util import db
from kleiderkammer.util.oidc import oidc

print("Starting...")

app = Flask(__name__)
app.config.from_prefixed_env()

# register blueprints
app.register_blueprint(kleidung, url_prefix='/kleidung')
app.register_blueprint(kleidung_api, url_prefix='/api/kleidung')
app.register_blueprint(mitglieder, url_prefix='/mitglieder')
app.register_blueprint(mitglieder_api, url_prefix='/api/mitglieder')
app.register_blueprint(einstellungen, url_prefix='/einstellungen')
app.register_blueprint(einstellungen_api, url_prefix='/api/einstellungen')

# initialize oidc
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


@oidc.require_login
@app.route("/")
def index():
    return redirect(app.url_for('kleidung.index'))


if __name__ == '__main__':
    # local testing only. Uwsgi does not call this method
    app.run()
