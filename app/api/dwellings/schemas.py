from marshmallow import fields, Schema, validate
from app.api.dwellings.models import Dwelling

class DwellingSchema(Schema):
    id = fields.Integer(dump_only=True)
    address = fields.String(required=True, validate=[validate.Length(min=4, max=255)])
    bedrooms = fields.Integer(required=True, validate=[validate.Range(min=1, error='Bedrooms must be at least 1.')])
    price = fields.Float(required=True, validate=[validate.Range(min=0.01, error='Price must be at least 0.01.')])

    class Meta:
        model = Dwelling
        load_instance = True
