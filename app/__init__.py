from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.secret_key = b"secret"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

with app.app_context():
    from app.api import api_bp
    app.register_blueprint(api_bp)

    from app.portfolio import portfolio_bp
    app.register_blueprint(portfolio_bp)

    from app.cookies import cookies_bp
    app.register_blueprint(cookies_bp)

from app import models, views, forms


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
