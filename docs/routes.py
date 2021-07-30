from flask import Flask, request, send_from_directory
from flask_login import (
    LoginManager,
    current_user,
    # login_required,
    # login_user,
    # logout_user,
)


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return (
            '<div><a class="button" href="/saga">Documentação Saga</a>'
            '<br>'
            '<a class="button" href="/aiolia">Documentação Aiolia</a></div>'
        )
    else:
        return '<a class="button" href="/login">Google Login</a></div>'


@app.route("/login")
def login():
    return 'Autenticar o user'


""" @app.route("/saga")
def send_saga_home():
    return send_from_directory("saga/0.1.0/docs/html", "home.html")


@app.route("/aiolia")
def send_aiolia_home():
    return send_from_directory("aiolia/0.3.1/docs/html", "index.html") """


@app.route('/<path:path>')
def send_page(path):
    if path == 'saga':
        return send_from_directory("saga/0.1.0/docs/html", "home.html")
    elif path == 'aiolia':
        return send_from_directory("aiolia/0.3.1/docs/html", "index.html")

    file_name = path.split("/")[-1]
    path_without_file = path.replace(file_name, "")
    return send_from_directory(path_without_file, file_name)


if __name__ == "__main__":
    app.run()
