from flask import Blueprint

todos_bp = Blueprint("todos", __name__, template_folder="templates", static_folder="static")
from . import views
