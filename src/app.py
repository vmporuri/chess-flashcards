from typing import Optional

from flask import Flask
from flask_session import Session
from src.auth import bcrypt
from src.models import User, db
from src.routes import login_manager, oauth, register_routes
from src.config import Config
from src.db import rq

sess = Session()


def create_app() -> Flask:
    """Factory function that generates a Flask app with configs set."""
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="../static/",
        template_folder="../templates/",
    )
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)
    oauth.init_app(app)
    rq.init_app(app)

    register_routes(app)
    oauth.register("lichess", client_kwargs={"code_challenge_method": "S256"})

    login_manager.login_view = "login_get"

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id) -> Optional[User]:
        return db.session.get(User, user_id)

    return app
