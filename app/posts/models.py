from .. import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Enum
import enum
from datetime import datetime
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship

post_tag_association = db.Table(
    'post_tag_association',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag {self.name}>"
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
    enabled = db.Column(db.Boolean, default=True)  # Corrected from 'enable'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    #category = db.relationship('Category', backref=db.backref('posts', lazy=True))
    tags = relationship('Tag', secondary=post_tag_association, backref=db.backref('posts', lazy=True))
    tags = relationship('Tag', secondary=post_tag_association, backref='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.created}')"
