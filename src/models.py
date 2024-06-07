import pydantic
import sqlmodel


# SQLModel Schema
class User(sqlmodel.SQLModel, table=True):
    user_id: int | None = sqlmodel.Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    lichess_username: str | None
    token: str | None


class Puzzle(sqlmodel.SQLModel, table=True):
    puzzle_id: int | None = sqlmodel.Field(default=None, primary_key=True)
    user_id: int | None = sqlmodel.Field(default=None, foreign_key="user.user_id")
    timestamp: int = sqlmodel.Field(ge=1356998400070)
    fen: str = sqlmodel.Field(max_length=100)
    solution: str = sqlmodel.Field(max_length=5)


# Pydantic Schema
class MoveModel(pydantic.BaseModel):
    move: str = pydantic.Field(pattern=r"^([a-h][1-8]){2}[qrbn]?$")


class ValidationModel(pydantic.BaseModel):
    isValidMove: bool
