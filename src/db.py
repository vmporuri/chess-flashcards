from sqlmodel import create_engine
from src import models

sqlite_file_name = "./databases/user_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def add_games_to_db():
    raise NotImplementedError()
