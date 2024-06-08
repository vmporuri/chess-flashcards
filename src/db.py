from typing import Generator

from src.models import db, Puzzle, User
from flask_bcrypt import Bcrypt

USER_EXISTS = -1

bcrypt = Bcrypt()


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


def register_new_user(user_data: dict[str, str]) -> int:
    username = user_data["username"]
    if User.query.filter_by(username=username).first() is not None:
        return USER_EXISTS
    hashed_password = bcrypt.generate_password_hash(user_data["password"])
    new_user = User(username=username, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print(new_user.user_id)
    return new_user.user_id
