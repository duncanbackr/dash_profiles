from flask import Blueprint

bp = Blueprint('hello', __name__)


@bp.route('/')
def world():
    return 'Hello, World!'
