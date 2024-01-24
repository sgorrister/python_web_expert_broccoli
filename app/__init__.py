from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'accounting.login'

    with app.app_context():
        from app.api import api_bp
        app.register_blueprint(api_bp)

        from app.portfolio import portfolio_bp
        app.register_blueprint(portfolio_bp)

        from app.cookies import cookies_bp
        app.register_blueprint(cookies_bp)

        from app.accounting import accounting_bp
        app.register_blueprint(accounting_bp)

        from app.todos import todos_bp
        app.register_blueprint(todos_bp)

        from app.feedback import feedback_bp
        app.register_blueprint(feedback_bp)

        from app.posts import posts_bp
        app.register_blueprint(posts_bp)

        from app.tests import tests_bp
        app.register_blueprint(tests_bp)

        from app import models, views, forms

    return app
