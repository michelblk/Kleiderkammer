from flask import Blueprint

from kleiderkammer.util.oidc import oidc

api = Blueprint('einstellungen_api', __name__)


@api.route('/', methods=['GET'])
@oidc.require_login
def get_all_einstellungen():
    return "passed"
