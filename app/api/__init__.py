from flask import Blueprint
api_bp = Blueprint("api", __name__, url_prefix='/api')
from .dwellings import dwellings_bp
api_bp.register_blueprint(dwellings_bp)

