from typing import Optional

from flask_bcrypt import Bcrypt
from src.models import LichessUser, User, db

bcrypt = Bcrypt()


def register_new_user(username: str, password: str) -> Optional[User]:
    """Signs up a new user in the database USERNAME isn't already used."""
    stmt = db.select(User).filter_by(username=username)
    old_user = db.session.scalars(stmt).first()
    if old_user is not None:
        return None
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def verify_login_credentials(username: str, password: str) -> Optional[User]:
    """Checks USERNAME and PASSWORD against stored credentials."""
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalars(stmt).first()
    if user is None or not bcrypt.check_password_hash(user.hashed_password, password):
        return None
    return user


def add_oauth_token(user_id, lichess_username, token, expires) -> None:
    """Adds Lichess OAuth token to account with USER_ID."""
    new_lichess_user = LichessUser(
        user_id=user_id, lichess_username=lichess_username, token=token, expires=expires
    )
    db.session.add(new_lichess_user)
    db.session.commit()
