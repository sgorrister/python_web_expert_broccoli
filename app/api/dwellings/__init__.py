from flask import Blueprint, jsonify
from marshmallow import ValidationError
from flask_restful import Api
from app.api.dwellings.controller import DwellingAPI, DwellingsAPI

dwellings_bp = Blueprint("dwellings", __name__)
api = Api(dwellings_bp, errors=dwellings_bp.app_errorhandler)

api.add_resource(DwellingAPI, "/dwelling", "/dwelling/<int:dwelling_id>")
api.add_resource(DwellingsAPI, "/dwellings")


@dwellings_bp.app_errorhandler(ValidationError)
def handle_marsmallow_error(error):
    return jsonify(error.messages), 400
