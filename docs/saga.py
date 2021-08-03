from flask import send_from_directory, Blueprint

saga = Blueprint('saga', __name__)


@saga.route('/path:<path>')
def send_saga_page(path):
    if path == 'saga':
        return send_from_directory("saga/0.1.0/docs/html", "home.html")

    file_name = path.split("/")[-1]
    return send_from_directory("saga/0.1.0/docs/html", file_name)
