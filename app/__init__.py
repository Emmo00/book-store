from flask import Flask
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

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    FlaskStatus(app)

    return app
