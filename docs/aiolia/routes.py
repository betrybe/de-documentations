from flask import send_from_directory, Blueprint

aiolia_route = Blueprint("aiolia", __name__)


@aiolia_route.route("/<path>")
def send_aiolia_page(path):
    return send_from_directory("aiolia/0.3.1/docs/html", path)


@aiolia_route.route("/_static/<path>")
def send_aiolia_static_stuff(path):
    return send_from_directory("aiolia/0.3.1/docs/html/_static", path)


@aiolia_route.route("/_static/css/<path>")
def send_aiolia_static_css_stuff(path):
    return send_from_directory("aiolia/0.3.1/docs/html/_static/css", path)


@aiolia_route.route("/_static/css/fonts/<path>")
def send_aiolia_static_css_font_stuff(path):
    return send_from_directory("aiolia/0.3.1/docs/html/_static/css/fonts", path)


@aiolia_route.route("/_static/js/<path>")
def send_aiolia_static_js_stuff(path):
    return send_from_directory("aiolia/0.3.1/docs/html/_static/js", path)
