from os import getenv


class Config:
    SECRET_KEY = getenv("SECRET_KEY") or "secret_key"
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI") or "sqlite:///verasworld.db"
