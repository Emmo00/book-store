import os

from flask import Flask, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_status import FlaskStatus
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    FlaskStatus(app)

    from app.views import client_bp
    from app.views.admin import admin_bp
    from app.views.api import api_bp

    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    app.static_folder = "public"

    return app
