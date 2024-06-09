import io

import urllib3
from src.puzzle_generator.generate_puzzles import find_all_mistakes
from src.puzzle_generator.db import add_games_to_db


def stream_games(username: str, headers: dict[str, str]) -> None:
    url = f"https://lichess.org/api/games/user/{username}?analysed=true&literate=true&accuracy=true"
    resp = urllib3.request(
        "GET",
        url,
        headers=headers,
        preload_content=False,
    )
    with io.TextIOWrapper(resp) as reader:  # type: ignore
        add_games_to_db(find_all_mistakes(reader))
    resp.release_conn()
