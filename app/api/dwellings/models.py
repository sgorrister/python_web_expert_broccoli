from app import db

class Dwelling(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    bedrooms = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"<Dwelling {self.id}: {self.address}>"