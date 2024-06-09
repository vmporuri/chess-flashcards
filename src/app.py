from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

oauth = OAuth()
bcrypt = Bcrypt()
login_manager = LoginManager()
sess = Session()
db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="../static/",
        template_folder="../templates/",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_data.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db
    app.config["SESSION_CLEANUP_N_REQUESTS"] = 100

    app.config["LICHESS_AUTHORIZE_URL"] = "https://lichess.org/oauth"
    app.config["LICHESS_ACCESS_TOKEN_URL"] = "https://lichess.org/api/token"
    # NOTE: Set a secure SECRET_KEY and LICHESS_CLIENT_ID in a .env file when not
    # running in a development environment. Then, replace the following lines with
    # the commented out lines.
    app.config["SECRET_KEY"] = "dummy-key"
    app.config["LICHESS_CLIENT_ID"] = "chess-flashcards"
    # import os
    # from dotenv import load_dotenv
    # load_dotenv("../.env")
    # app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    # app.config["LICHESS_CLIENT_ID"] = os.getenv("LICHESS_CLIENT_ID")

    db.init_app(app)
    oauth.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)

    login_manager.login_view = "login_get"

    oauth.register("lichess", client_kwargs={"code_challenge_method": "S256"})

    return app
