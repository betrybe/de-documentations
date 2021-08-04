from flask import Flask, redirect, request, url_for, send_from_directory, Blueprint



saga_routes = Blueprint('saga_routes', __name__)


@saga_routes.route('/<path>')
def send_saga_page(path):
    return send_from_directory("saga/0.1.0/docs/html", path)


@saga_routes.route('/_static/<path>')
def send_static_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static', path)


@saga_routes.route('/_static/css/<path>')
def send_static_css_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/css', path)


@saga_routes.route('/_static/css/fonts/<path>')
def send_static_css_font_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/css/fonts', path)


@saga_routes.route('/_static/js/<path>')
def send_static_js_stuff(path):
    return send_from_directory('saga/0.1.0/docs/html/_static/js', path)
