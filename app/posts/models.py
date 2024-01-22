from .. import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import enum
from datetime import datetime

class EnumPriority(enum.Enum):
    low = 1
    medium = 2
    high = 3

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), default='postdefault.jpg')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(Enum(EnumPriority), default='low')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.created}')"
