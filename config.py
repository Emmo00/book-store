from datetime import timedelta
from os import getenv


class Config:
    SECRET_KEY = getenv("SECRET_KEY") or "secret_key"
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI") or "sqlite:///verasworld.db"
    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    SESSION_COOKIE_NAME = "X-Auth"
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=315360000)
    BOOKS_PER_PAGE = 16
