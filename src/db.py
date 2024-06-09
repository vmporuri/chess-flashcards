from typing import Generator, Optional

from src.app import bcrypt, db, login_manager
from src.models import Puzzle, User


def add_games_to_db(
    puzzles: Generator[Puzzle, None, None],
    user_id: int,
    batch_size: int = 50,
) -> None:
    batch = 0
    for puzzle in puzzles:
        puzzle.user_id = user_id
        db.session.add(puzzle)
        if batch >= batch_size:
            batch = 0
            db.session.commit()

    db.session.commit()


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


@login_manager.user_loader
def load_user(user_id) -> Optional[User]:
    return User.query.get(user_id)
