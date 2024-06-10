from typing import Generator, TextIO

import chess.pgn
import src.puzzle_generator.time_utils as time_utils
from src.models import Puzzle


def generate_puzzles_from_game(pgn_stream: TextIO) -> Generator[Puzzle, None, None]:
    """A generator function that yields puzzles from one game.

    Note: Only pushes PGN_STREAM forward by one game.
    """
    game = chess.pgn.read_game(pgn_stream)
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
            yield Puzzle(
                timestamp=timestamp,
                fen=fen,
                solution=str(prev_move.variations[1].move),
            )
        prev_move = curr_move
        curr_move = curr_move.next()


def generate_puzzles(pgn_stream: TextIO) -> Generator[Puzzle, None, None]:
    """Provided a stream of pgns, yields puzzles from each game.

    Note: PGN_STREAM must close automatically after all lines are read.
    """
    while not pgn_stream.closed:
        yield from generate_puzzles_from_game(pgn_stream)
