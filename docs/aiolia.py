from flask import send_from_directory, Blueprint

aiolia = Blueprint('aiolia', __name__)


@aiolia.route('/path:<path>')
def send_aiolia_page(path):
    if path == 'aiolia':
        return send_from_directory("aiolia/0.3.1/docs/html", "index.html")

    file_name = path.split("/")[-1]
    return send_from_directory("aiolia/0.3.1/docs/html", file_name)
