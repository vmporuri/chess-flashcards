from urllib3 import BaseHTTPResponse, request

LICHESS_HOST = "https://lichess.org/api/games/user/"
QUERY_PARAMS = "?analysed=true&literate=true&accuracy=true"


def stream_games(
    lichess_username: str, timestamp: int, headers: dict[str, str]
) -> BaseHTTPResponse:
    """Returns a stream of pgns of games played by LICHESS_USERNAME after TIMESTAMP."""
    url = f"{LICHESS_HOST}{lichess_username}{QUERY_PARAMS}&since={timestamp}"
    return request(
        "GET",
        url,
        headers=headers,
        preload_content=False,
    )
