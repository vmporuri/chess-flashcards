from typing import Annotated, Generator, TextIO

import chess.pgn
import src.time_utils as time_utils
from pydantic import BaseModel, Field, conint


class Position(BaseModel):
    timestamp: Annotated[int, conint(ge=1356998400070)]
    fen: str = Field(
        pattern=r"^((?:[1-8PNBRQKpnbrqk]+\/){7}[1-8PNBRQKpnbrqk]+) ([wb]) (K?Q?k?q?|-) ([a-h][1-8]|-) (\d+) (\d+)$"
    )
    solution: str = Field(pattern=r"^([a-h][1-8]){2}$")


def find_mistakes_in_one_game(pgn: TextIO) -> Generator[Position, None, None]:
    game = chess.pgn.read_game(pgn)
    if game is None:
        return
    timestamp = time_utils.convert_utc_to_unix(
        game.headers["UTCDate"], game.headers["UTCTime"]
    )
    curr_move = game.next()
    prev_move = None
    while curr_move is not None:
        if prev_move is not None and "was best" in curr_move.comment:
            fen = prev_move.board().fen()
            yield Position(
                timestamp=timestamp,
                fen=fen,
                solution=str(prev_move.variations[1].move),
            )
        prev_move = curr_move
        curr_move = curr_move.next()


def find_all_mistakes(pgn: TextIO) -> Generator[Position, None, None]:
    while not pgn.closed:
        yield from find_mistakes_in_one_game(pgn)
