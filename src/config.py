from src.models import db


class Config:
    """Config attributes for Flask app."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///user_data.db"
    SQLALCHEMY_ECHO = True
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY = db

    LICHESS_AUTHORIZE_URL = "https://lichess.org/oauth"
    LICHESS_ACCESS_TOKEN_URL = "https://lichess.org/api/token"
    # NOTE: Set a secure SECRET_KEY and LICHESS_CLIENT_ID in a .env file when not
    # running in a development environment. Then, replace the following lines with
    # the commented out lines.
    SECRET_KEY = "dummy-key"
    LICHESS_CLIENT_ID = "chess-flashcards"
    # import os
    # from dotenv import load_dotenv
    # load_dotenv("../.env")
    # SECRET_KEY = os.getenv("SECRET_KEY")
    # LICHESS_CLIENT_ID = os.getenv("LICHESS_CLIENT_ID")
