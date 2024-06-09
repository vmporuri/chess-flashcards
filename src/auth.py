from typing import Optional

from flask_bcrypt import Bcrypt
from src.models import User, db

bcrypt = Bcrypt()


def register_new_user(username: str, password: str) -> Optional[User]:
    if User.query.filter_by(username=username).first() is not None:
        return None
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def verify_login_credentials(username: str, password: str) -> Optional[User]:
    user = User.query.filter_by(username=username).first()
    if user is None or not bcrypt.check_password_hash(user.hashed_password, password):
        return None
    return user
