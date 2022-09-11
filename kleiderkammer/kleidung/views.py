from flask import Blueprint, render_template

from kleiderkammer.kleidung.model.kleidung import Kleidung
from kleiderkammer.util.oidc import oidc

kleidung = Blueprint('kleidung', __name__, template_folder="templates")


@kleidung.route("/", methods=['GET'])
@oidc.require_login
def index():
    rows = Kleidung.query\
        .filter_by(archiviert=False)\
        .order_by(Kleidung.code)\
        .all()

    return render_template("kleidung.html", rows=rows)
