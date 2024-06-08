from typing import Generator
from sqlmodel import Session, create_engine
from src import models

sqlite_file_name = "./databases/user_data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def add_games_to_db(
    puzzles: Generator[models.Puzzle, None, None],
    batch_size: int = 50,
) -> None:
    with Session(engine) as session:
        batch = []
        for puzzle in puzzles:
            batch.append(puzzle)
            if len(batch) >= batch_size:
                session.add_all(batch)
                session.commit()
                batch.clear()

        if batch:
            session.add_all(batch)
        session.commit()
