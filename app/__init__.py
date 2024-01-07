from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_status import FlaskStatus
from flask_migrate import Migrate
from flask_session import Session


db = SQLAlchemy()
migrate = Migrate()


def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)
    app.config["SESSION_SQLALCHEMY"] = db

    db.init_app(app)
    migrate.init_app(app, db)
    FlaskStatus(app)
    Session(app)

    from app.views import client_bp
    from app.views.admin import admin_bp
    from app.views.api import api_bp

    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    app.static_folder = "public"

    return app
