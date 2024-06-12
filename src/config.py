import os

from dotenv import load_dotenv
from src.models import db

load_dotenv(".env")


class Config:
    """Config attributes for Flask app."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///user_data.db"
    SQLALCHEMY_ECHO = True
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY = db

    LICHESS_AUTHORIZE_URL = "https://lichess.org/oauth"
    LICHESS_ACCESS_TOKEN_URL = "https://lichess.org/api/token"
    LICHESS_CLIENT_ID = os.getenv("LICHESS_CLIENT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
