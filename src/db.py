from io import TextIOWrapper
from typing import Optional

from flask_rq2 import RQ
from sqlalchemy import func

from src.models import LichessUser, Puzzle, db
from src.puzzle_generator.generate_puzzles import generate_puzzles
from src.puzzle_generator.lichess_api import stream_games

ONE_SECOND_IN_MS = 1000
DEFAULT_TIMESTAMP = 1356998400070

rq = RQ()


def fetch_random_puzzle_fen(user_id: int) -> tuple[str, str]:
    """Fetches a random puzzle from the database."""
    stmt = db.select(Puzzle).filter_by(user_id=user_id).order_by(func.random()).limit(1)
    puzzle = db.session.scalars(stmt).first()
    if puzzle is None:
        return "", ""
    return puzzle.fen, puzzle.solution


@rq.job
def add_puzzles_to_db(lichess_user: LichessUser) -> None:
    """Fetches any new games played by LICHESS_USER and adds generated puzzles to DB."""
    if (recent_puzzle := find_newest_puzzle(lichess_user)) is not None:
        timestamp = recent_puzzle.timestamp + ONE_SECOND_IN_MS
    else:
        timestamp = DEFAULT_TIMESTAMP
    token = lichess_user.token
    headers = {"Authorization": f"Bearer {token}"}
    with stream_games(lichess_user.lichess_username, timestamp, headers) as http_stream:
        with TextIOWrapper(http_stream) as pgn_stream:
            for puzzle in generate_puzzles(pgn_stream, lichess_user.lichess_username):
                add_puzzle(puzzle, lichess_user.user_id)


def add_puzzle(puzzle: Puzzle, user_id: int) -> None:
    """Adds a single PUZZLE to DB."""
    puzzle.user_id = user_id
    db.session.add(puzzle)
    db.session.commit()


def find_newest_puzzle(lichess_user: LichessUser) -> Optional[Puzzle]:
    """Fetches the puzzle with most recent timestamp in the database if it exists."""
    stmt = (
        db.select(Puzzle)
        .filter_by(user_id=lichess_user.user_id)
        .order_by(Puzzle.timestamp.desc())
        .limit(1)
    )
    return db.session.scalars(stmt).first()


def update_puzzle_registries(batch_size=10) -> None:
    """For each user, generates new puzzles from recent Lichess games."""
    stmt = db.select(LichessUser).execution_options(yield_per=batch_size)
    for lichess_user in db.session.scalars(stmt):
        add_puzzles_to_db(lichess_user)
