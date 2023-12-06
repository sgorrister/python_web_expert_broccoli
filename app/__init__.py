from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.secret_key = b"secret"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import views, models, forms

from app import views

