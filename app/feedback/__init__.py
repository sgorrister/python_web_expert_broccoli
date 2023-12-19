from flask import Blueprint

feedback_bp = Blueprint("feedback", __name__, template_folder="templates", static_folder="static")
from . import views
