from urllib3 import BaseHTTPResponse, request

LICHESS_HOST = "https://lichess.org/api/games/user/"
QUERY_PARAMS = "?analysed=true&literate=true&accuracy=true"


def stream_games(lichess_username: str, headers: dict[str, str]) -> BaseHTTPResponse:
    url = f"{LICHESS_HOST}{lichess_username}{QUERY_PARAMS}"
    return request(
        "GET",
        url,
        headers=headers,
        preload_content=False,
    )
