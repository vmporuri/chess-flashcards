from flask_login import UserMixin
from src.app import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String, unique=True, nullable=False)
    hashed_password: str = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, username, hashed_password) -> None:
        self.username = username
        self.hashed_password = hashed_password

    def get_id(self) -> str:
        return str(self.user_id)


class LichessUser(db.Model):
    __tablename__ = "lichess_users"
    lichess_id: int = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    lichess_username: str = db.Column(db.String, unique=True, nullable=False)
    token: str = db.Column(db.String, unique=True, nullable=False)
    expires: int = db.Column(db.Integer, nullable=False)

    def __init__(self, lichess_username, token, expires) -> None:
        self.lichess_username = lichess_username
        self.token = token
        self.expires = expires


class Puzzle(db.Model):
    __tablename__ = "puzzles"
    puzzle_id: int | None = db.Column(db.Integer, primary_key=True)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    timestamp: int = db.Column(db.Integer, nullable=False)
    fen: str = db.Column(db.String, unique=True, nullable=False)
    solution: str = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, timestamp, fen, solution) -> None:
        self.timestamp = timestamp
        self.fen = fen
        self.solution = solution
