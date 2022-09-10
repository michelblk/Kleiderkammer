from flask import Blueprint

from kleiderkammer.util.oidc import oidc

api = Blueprint('einstellungen-api', __name__)


@api.route('/', methods=['GET'])
@oidc.accept_token(True, ['openid'])
def get_all_einstellungen():
    return "passed"
