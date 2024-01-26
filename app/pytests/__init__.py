from flask import Blueprint
from .. import db

pytests_bp = Blueprint('pytests', __name__, template_folder='templates', static_folder='static')
from . import views
