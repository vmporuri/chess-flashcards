import io

import urllib3
from src.chess_utils import find_all_mistakes

LICHESS_HOST = "https://lichess.org"


# TODO: Might be worth using an api endpoint to download games. That function can
# access the session data (since needs to be an api access to get session data)
# then asynchronously begin downloading (or use rq) and put redirect back
# TODO: Consider storing auth token in session (bearer) as per Flask suggestions
# for a proof of concept
# TODO: Also consider making session data not permanent again
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
