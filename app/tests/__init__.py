from flask import Blueprint
from .. import db

tests_bp = Blueprint('tests', __name__, template_folder='templates', static_folder='static')
from . import views
