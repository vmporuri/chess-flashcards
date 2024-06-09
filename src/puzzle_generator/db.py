from typing import Generator

from src.models import Puzzle, db


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
