from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)

    lichess_user: Mapped["LichessUser"] = relationship(back_populates="user")
    puzzles: Mapped[list["Puzzle"]] = relationship(back_populates="user")

    def get_id(self) -> str:
        return str(self.user_id)


class LichessUser(db.Model):
    __tablename__ = "lichess_users"

    lichess_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    lichess_username: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(nullable=False)
    expires: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="lichess_user")


class Puzzle(db.Model):
    __tablename__ = "puzzles"

    puzzle_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    timestamp: Mapped[int] = mapped_column(nullable=False)
    fen: Mapped[str] = mapped_column(nullable=False)
    solution: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship(back_populates="puzzles")
