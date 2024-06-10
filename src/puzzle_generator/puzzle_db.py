from flask_sqlalchemy import SQLAlchemy
from puzzle_generator.generate_puzzles import generate_puzzles
from puzzle_generator.lichess_api import stream_games
from src.models import LichessUser, Puzzle
from io import TextIOWrapper


def add_puzzles_to_db(db: SQLAlchemy, lichess_user: LichessUser) -> None:
    token = lichess_user.token
    headers = {"Authorization": f"Bearer {token}"}
    with stream_games(lichess_user.lichess_username, headers) as http_stream:
        with TextIOWrapper(http_stream) as pgn_stream:
            for puzzle in generate_puzzles(pgn_stream):
                add_puzzle(db, puzzle, lichess_user.user_id)


def add_puzzle(db: SQLAlchemy, puzzle: Puzzle, user_id: int) -> None:
    puzzle.user_id = user_id
    db.session.add(puzzle)
    db.session.commit()
