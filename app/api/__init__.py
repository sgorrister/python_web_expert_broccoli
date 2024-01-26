from flask import Blueprint
api_bp = Blueprint("api", __name__, url_prefix='/api')
from .dwellings import dwellings_bp
api_bp.register_blueprint(dwellings_bp)
from . import controller
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

jwt = JWTManager()