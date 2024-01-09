from datetime import timedelta
from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = getenv("SECRET_KEY") or "secret_key"
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI") or "sqlite:///verasworld.db"
    SESSION_TYPE = "sqlalchemy"
    SESSION_PERMANENT = True
    SESSION_COOKIE_NAME = "X-Auth"
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=315360000)
    BOOKS_PER_PAGE = 16
    UPLOADS_FOLDER = getenv("UPLOADS_FOLDER") or "uploads"
    ADMIN_USER = getenv("ADMIN_USER") or "admin"
    ADMIN_PASS = getenv("ADMIN_PASS") or "admin"
