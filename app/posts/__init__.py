from flask import Blueprint
from .. import db

posts_bp = Blueprint('posts', __name__, template_folder='templates', static_folder='static')
from . import views
