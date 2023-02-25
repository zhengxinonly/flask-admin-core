from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .init_jwt import register_jwt

db = SQLAlchemy()


def register_extension(app: Flask):
    db.init_app(app)
    register_jwt(app)
