from src.chess_utils import find_mistakes


sample_game = """
[Event "Rated bullet game"]
[Site "https://lichess.org/Qk15DnVA"]
[Date "2024.06.02"]
[White "eoiz"]
[Black "VexinglyPerplexing"]
[Result "1-0"]
[UTCDate "2024.06.02"]
[UTCTime "20:12:56"]
[WhiteElo "1375"]
[BlackElo "1500"]
[WhiteRatingDiff "+4"]
[BlackRatingDiff "-342"]
[Variant "Standard"]
[TimeControl "60+0"]
[ECO "D00"]
[Opening "Queen's Pawn Game: Chigorin Variation"]
[Termination "Normal"]
[Annotator "lichess.org"]

1. d4 d5 2. Nc3 { D00 Queen's Pawn Game: Chigorin Variation } Nc6 3. Bf4 Nf6?! { (0.15 → 0.72) Inaccuracy. a6 was best. } (3... a6 4. a3 Nf6 5. e3 Bf5 6. Bd3 Bxd3 7. Qxd3 e6 8. Nf3) 4. Nb5 e6?? { (0.66 → 3.76) Blunder. e5 was best. } (4... e5 5. Bxe5 Nxe5 6. dxe5 a6 7. Nc3 d4 8. exf6 dxc3 9. Qxd8+) 5. Nxc7+ Qxc7?! { (4.17 → 5.57) Inaccuracy. Kd7 was best. } (5... Kd7 6. Nxa8 Bd6 7. Bxd6 Kxd6 8. e3 Bd7 9. Bd3 Ke7 10. Qd2) 6. Bxc7 Bd7 7. Bg3 Be7 8. Nf3 O-O 9. e3 Rfe8 10. Bb5 Rad8 11. Bxc6 bxc6 12. Ne5 Bc8 13. O-O Ba6 14. Re1 Bd6 15. Nxc6 Bxg3 16. Nxd8 Bxf2+ 17. Kxf2 Rxd8 18. b3 Ne4+ 19. Kg1 Nc3 20. Qd2 Ne4 21. Qa5 Bc8?? { (5.76 → Mate in 1) Checkmate is now unavoidable. Rf8 was best. } (21... Rf8 22. Qxa6 h5 23. Qf1 f5 24. c4 g5 25. Re2 f4 26. Qe1 fxe3 27. Rxe3) 22. Qxd8# { White wins by checkmate. } 1-0
"""


def test_convert_pgn_to_game() -> None:
    actual = find_mistakes(sample_game)
    expected_timestamps = [1717359176000] * len(actual)
    expected_fens = [
        "r1bqkbnr/ppp1pppp/2n5/3p4/3P1B2/2N5/PPP1PPPP/R2QKBNR b KQkq - 3 3",
        "r1bqkb1r/ppp1pppp/2n2n2/1N1p4/3P1B2/8/PPP1PPPP/R2QKBNR b KQkq - 5 4",
        "r1bqkb1r/ppN2ppp/2n1pn2/3p4/3P1B2/8/PPP1PPPP/R2QKBNR b KQkq - 0 5",
        "3r2k1/p4ppp/b3p3/Q2p4/3Pn3/1P2P3/P1P3PP/R3R1K1 b - - 6 21",
    ]
    expected_solutions = [
        "a7a6",
        "e7e5",
        "e8d7",
        "d8f8",
    ]

    for i in range(len(actual)):
        assert actual[i].timestamp == expected_timestamps[i]
        assert actual[i].fen == expected_fens[i]
        assert actual[i].solution == expected_solutions[i]
