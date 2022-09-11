SECRET_KEY = 'SomethingNotEntirelySecret'
TESTING = True
DEBUG = True
OIDC_CLIENT_SECRETS = 'client_secrets.json'
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_REQUIRE_VERIFIED_EMAIL = False
OIDC_OPENID_REALM = 'http://localhost:5000/oidc_callback'
OIDC_SCOPES = ['openid', 'email', 'profile']
OIDC_COOKIE_SECURE = False

SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:mariadb@127.0.0.1:3306/kleiderkammer'
