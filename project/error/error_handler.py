from flask import Blueprint, jsonify, render_template, make_response


errorpage_blueprint = Blueprint('error', '__name__', template_folder='templates', static_folder='static')


@errorpage_blueprint.app_errorhandler(403)
def error_403(e):
    return make_response(render_template('error-403.html'))


@errorpage_blueprint.app_errorhandler(404)
def error_404(e):
    return make_response(render_template('error-404.html'))


@errorpage_blueprint.app_errorhandler(405)
def error_405(e):
    return make_response(render_template('error-405.html'))


@errorpage_blueprint.app_errorhandler(500)
def error_500(e):
    return make_response(render_template('error-500.html'))