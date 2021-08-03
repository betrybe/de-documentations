import json
import os
import sqlite3

from flask import Flask, redirect, request, url_for, send_from_directory, Blueprint
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from sso_authentication.db import init_db_command
from sso_authentication.user import User

from saga import saga
from aiolia import aiolia

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.register_blueprint(saga, url_prefix='/saga')
app.register_blueprint(aiolia, url_prefix='/aiolia')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass

client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            '<div><a class="button" href="/saga">Documentação Saga</a>'
            '<br>'
            '<a class="button" href="/aiolia">Documentação Aiolia</a></div>'.format(
                current_user.name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a></div>'


@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    print(userinfo_endpoint)
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect(url_for("index"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/_static/<path>')
def send_static_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static', path)


@app.route('/_static/css/<path>')
def send_static_css_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/css', path)


@app.route('/_static/css/fonts/<path>')
def send_static_css_font_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/css/fonts', path)


@app.route('/_static/js/<path>')
def send_static_js_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/js', path)


@app.route('/_static/<path>')
def send_aiolia_static_stuff(path):
    return send_from_directory('aiolia/0.3.1/docs/html/html/_static', path)


@app.route('/_static/css/<path>')
def send_aiolia_static_css_stuff(path):
    return send_from_directory('aiolia/0.3.1/docs/html/html/_static/css', path)


@app.route('/_static/css/fonts/<path>')
def send_aiolia_static_css_font_stuff(path):
    return send_from_directory('aiolia/0.3.1/docs/html/html/_static/css/fonts', path)


@app.route('/_static/js/<path>')
def send_aiolia_static_js_stuff(path):
    return send_from_directory('aiolia/0.3.1/docs/html/html/_static/js', path)


# url = url_for('saga.send_saga_page')


""" @app.route('/<path:path>')
def send_saga_page(path):
    if path == 'saga':
        return send_from_directory("saga/0.1.0/docs/html", "home.html")

    file_name = path.split("/")[-1]
    return send_from_directory("saga/0.1.0/docs/html", file_name) """


""" @app.route('/aiolia/<path:path>')
def send_aiolia_page(path):
    if path == 'aiolia':
        return send_from_directory("aiolia/0.3.1/docs/html", "index.html")

    file_name = path.split("/")[-1]
    print(f"file_name: {file_name}")
    print(f"path fora do aiolia/home: {path}")
    return send_from_directory("aiolia/0.3.1/docs/html", file_name) """


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
