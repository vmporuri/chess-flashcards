from sqlalchemy import func
from src.models import Puzzle, db


def fetch_random_puzzle_fen(user_id: int) -> tuple[str, str]:
    stmt = db.select(Puzzle).filter_by(user_id=user_id).order_by(func.random()).limit(1)
    puzzle = db.session.scalars(stmt).first()
    if puzzle is None:
        return "", ""
    return puzzle.fen, puzzle.solution
