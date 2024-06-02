import io
import re
from typing import List

import chess.pgn
from pydantic import BaseModel, Field, field_validator


class Move(BaseModel):
    fen: str = Field()
    solution: str = Field(pattern=r"^([a-h][1-8]){2}$")

    @field_validator("fen")
    def validate_fen(cls, v):
        pattern = re.compile(r"^([1-8PNBRQK]+\/){7}[1-8PNBRQK]+ [wb]$", re.IGNORECASE)
        if not pattern.match(v):
            raise ValueError("Invalid FEN format")
        return v


def convert_pgn_to_game(pgn: str) -> chess.pgn.Game:
    pgnIO = io.StringIO(pgn)
    game = chess.pgn.read_game(pgnIO)
    if game is None:
        raise ValueError("Not a valid PGN")
    return game


def find_mistakes(pgn: str) -> List[Move]:
    game = convert_pgn_to_game(pgn)
    mistakes = []
    # print(game.headers["UTCDate"])
    # print(game.headers["UTCTime"])
    curr_move = game.next()
    prev_move = None
    while curr_move is not None:
        if prev_move is not None and "was best" in curr_move.comment:
            print(curr_move.move)
            print(curr_move.comment)
            print(prev_move.variations[1].move)

            fen = " ".join(prev_move.board().fen().split()[:2])
            mistakes.append(Move(fen=fen, solution=str(prev_move.variations[1].move)))
        prev_move = curr_move
        curr_move = curr_move.next()
    return mistakes
