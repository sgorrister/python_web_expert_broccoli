from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.secret_key = b"secret"
app.config.from_object(Config)

from app import views, models, forms

from app import views
from app.models import db

db.init_app(app)
