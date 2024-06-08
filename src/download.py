import io

import urllib3
from src.db import add_games_to_db
from src.chess_utils import find_all_mistakes

LICHESS_HOST = "https://lichess.org"


def download_chess_games(username: str, headers: dict[str, str]) -> None:
    url = f"{LICHESS_HOST}/api/games/user/{username}?analysed=true&literate=true&accuracy=true"
    resp = urllib3.request(
        "GET",
        url,
        headers=headers,
        preload_content=False,
    )
    with io.TextIOWrapper(resp) as reader:  # type: ignore
        add_games_to_db(find_all_mistakes(reader))
    resp.release_conn()
