import io
from typing import Annotated

import chess.pgn
import src.time_utils as time_utils
from pydantic import BaseModel, Field, conint


class Position(BaseModel):
    timestamp: Annotated[int, conint(ge=1356998400070)]
    fen: str = Field(
        pattern=r"^((?:[1-8PNBRQKpnbrqk]+\/){7}[1-8PNBRQKpnbrqk]+) ([wb]) (K?Q?k?q?|-) ([a-h][1-8]|-) (\d+) (\d+)$"
    )
    solution: str = Field(pattern=r"^([a-h][1-8]){2}$")


class BoardState(BaseModel):
    timestamp: Annotated[int, conint(ge=1356998400070)]
    board: list[list[str]]
    turn: str = Field(pattern=r"[b|w]")
    solution: str = Field(pattern=r"^([a-h][1-8]){2}$")


def convert_pgn_to_game(pgn: str) -> chess.pgn.Game:
    pgnIO = io.StringIO(pgn)
    game = chess.pgn.read_game(pgnIO)
    if game is None:
        raise ValueError("Not a valid PGN")
    return game


def find_mistakes(pgn: str) -> list[Position]:
    game = convert_pgn_to_game(pgn)
    timestamp = time_utils.convert_utc_to_unix(
        game.headers["UTCDate"], game.headers["UTCTime"]
    )
    mistakes = []
    curr_move = game.next()
    prev_move = None
    while curr_move is not None:
        if prev_move is not None and "was best" in curr_move.comment:
            fen = prev_move.board().fen()
            mistakes.append(
                Position(
                    timestamp=timestamp,
                    fen=fen,
                    solution=str(prev_move.variations[1].move),
                )
            )
        prev_move = curr_move
        curr_move = curr_move.next()
    return mistakes


def get_board(pos: Position) -> BoardState:
    timestamp = pos.timestamp
    solution = pos.solution
    board: list[list[str]] = [
        row.split(" ") for row in str(chess.Board(pos.fen)).split("\n")
    ]
    turn = pos.fen.split()[1]
    return BoardState(timestamp=timestamp, board=board, turn=turn, solution=solution)
