import os
import sqlite3

from flask import Flask, redirect, request, url_for, send_from_directory, Blueprint
from flask_login import LoginManager, current_user


from sso_authentication.db import init_db_command
from sso_authentication.routes import login_routes

from saga.routes import saga_routes
from aiolia.routes import aiolia_route

from aiolia.routes import aiolia_route
from sso_authentication.user import User

app = Flask(__name__)
app.register_blueprint(saga_routes, url_prefix="/saga")
app.register_blueprint(aiolia_route, url_prefix="/aiolia")
app.register_blueprint(login_routes, url_prefix="/")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

try:
    init_db_command()
except sqlite3.OperationalError:
    pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            '<div><a class="button" href="/saga/home.html">Documentação Saga</a>'
            "<br>"
            '<a class="button" href="/aiolia/index.html">Documentação Aiolia</a></div>'.format(
                current_user.name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a></div>'


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
