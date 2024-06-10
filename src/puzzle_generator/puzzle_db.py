from io import TextIOWrapper
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from puzzle_generator.generate_puzzles import generate_puzzles
from puzzle_generator.lichess_api import stream_games
from src.models import LichessUser, Puzzle

DEFAULT_TIMESTAMP = 1356998400070
ONE_SECOND = 1000


def add_puzzles_to_db(db: SQLAlchemy, lichess_user: LichessUser) -> None:
    """Fetches any new games played by LICHESS_USER and adds generated puzzles to DB."""
    if (recent_puzzle := find_newest_puzzle(db, lichess_user)) is not None:
        timestamp = recent_puzzle.timestamp + ONE_SECOND
    else:
        timestamp = DEFAULT_TIMESTAMP
    token = lichess_user.token
    headers = {"Authorization": f"Bearer {token}"}
    with stream_games(lichess_user.lichess_username, timestamp, headers) as http_stream:
        with TextIOWrapper(http_stream) as pgn_stream:
            for puzzle in generate_puzzles(pgn_stream, lichess_user.lichess_username):
                add_puzzle(db, puzzle, lichess_user.user_id)


def add_puzzle(db: SQLAlchemy, puzzle: Puzzle, user_id: int) -> None:
    """Adds a single PUZZLE to DB."""
    puzzle.user_id = user_id
    db.session.add(puzzle)
    db.session.commit()


def find_newest_puzzle(db: SQLAlchemy, lichess_user: LichessUser) -> Optional[Puzzle]:
    """Fetches the puzzle with most recent timestamp in the database if it exists."""
    stmt = (
        db.select(Puzzle)
        .filter_by(user_id=lichess_user.user_id)
        .order_by(Puzzle.timestamp.desc())
        .limit(1)
    )
    return db.session.scalars(stmt).first()
