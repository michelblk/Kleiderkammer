import flask_login
from flask import Blueprint

api = Blueprint('einstellungen_api', __name__)


@api.route('/', methods=['GET'])
@flask_login.login_required
def get_all_einstellungen():
    return "passed"
