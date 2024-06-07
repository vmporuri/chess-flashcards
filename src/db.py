import io

import urllib3
from src.chess_utils import find_all_mistakes

LICHESS_HOST = "https://lichess.org"


def download_chess_games(username: str, headers: dict[str, str]):
    url = f"{LICHESS_HOST}/api/games/user/{username}?analysed=true&literate=true&accuracy=true"
    resp = urllib3.request(
        "GET",
        url,
        headers=headers,
        preload_content=False,
    )
    with io.TextIOWrapper(resp) as reader:  # type: ignore
        for mistake in find_all_mistakes(reader):
            print(mistake)
    resp.release_conn()


def add_games_to_db():
    raise NotImplementedError()
