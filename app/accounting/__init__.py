from flask import Blueprint

accounting_bp = Blueprint("accounting", __name__, template_folder="templates", static_folder="static")
from . import views
