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
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    posts = relationship('Post', backref='category', lazy=True)  # Relationship with Post model

    def __repr__(self):
        return f"<Category {self.name}>"
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), default='postdefault.jpg')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(Enum(EnumPriority), default='low')
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.created}')"
