from flask import request
from flask_restful import Resource
from app.api.dwellings.models import Dwelling
from app.api.dwellings.schemas import DwellingSchema
from app import db


class DwellingsAPI(Resource):
    def get(self):
        dwellings = Dwelling.query.all()
        schema = DwellingSchema(many=True)
        return schema.dump(dwellings)

    def post(self):
        data = request.get_json()
        new_dwelling = Dwelling(address=data['address'], bedrooms=data['bedrooms'], price=data['price'])
        db.session.add(new_dwelling)
        db.session.commit()
        return DwellingSchema().dump(new_dwelling), 201


class DwellingAPI(Resource):
    def get(self, dwelling_id):
        if dwelling_id:
            dwelling = Dwelling.query.get(dwelling_id)
            if dwelling:
                return DwellingSchema().dump(dwelling)
            return {"message": "Dwelling not found"}, 404
        else:
            dwellings = Dwelling.query.all()
            return DwellingSchema(many=True).dump(dwellings)

    def put(self, dwelling_id):
        dwelling = Dwelling.query.get(dwelling_id)
        if dwelling:
            data = request.get_json()
            dwelling.address = data['address']
            dwelling.bedrooms = data['bedrooms']
            dwelling.price = data['price']
            db.session.commit()
            return DwellingSchema().dump(dwelling)
        return {"message": "Dwelling not found"}, 404

    def delete(self, dwelling_id):
        dwelling = Dwelling.query.get(dwelling_id)
        if dwelling:
            db.session.delete(dwelling)
            db.session.commit()
            return {"message": "Dwelling deleted"}
        return {"message": "Dwelling not found"}, 404


