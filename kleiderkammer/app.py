import json

from flask import Flask, g, send_from_directory
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_COOKIE_SECURE': False
})
oidc = OpenIDConnect(app)


@app.route('/')
@app.route('/<path:path>')
def hello_world(path='index.html'):
    return send_from_directory('static/ui', path)


@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['email'])
    return ('Hello, %s! <a href="/">Return</a>' %
            (info.get('email')))


@app.route('/api')
@oidc.accept_token(True, ['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'


def start():
    app.run(host="0.0.0.0")
