import io

from src.puzzle_generator.generate_puzzles import (
    find_all_mistakes,
    find_mistakes_in_one_game,
)

sample_one_game = """
[UTCDate "2024.06.02"]
[UTCTime "20:12:56"]

1. d4 d5 2. Nc3 { D00 Queen's Pawn Game: Chigorin Variation } Nc6 3. Bf4 Nf6?! { (0.15 → 0.72) Inaccuracy. a6 was best. } (3... a6 4. a3 Nf6 5. e3 Bf5 6. Bd3 Bxd3 7. Qxd3 e6 8. Nf3) 4. Nb5 e6?? { (0.66 → 3.76) Blunder. e5 was best. } (4... e5 5. Bxe5 Nxe5 6. dxe5 a6 7. Nc3 d4 8. exf6 dxc3 9. Qxd8+) 5. Nxc7+ Qxc7?! { (4.17 → 5.57) Inaccuracy. Kd7 was best. } (5... Kd7 6. Nxa8 Bd6 7. Bxd6 Kxd6 8. e3 Bd7 9. Bd3 Ke7 10. Qd2) 6. Bxc7 Bd7 7. Bg3 Be7 8. Nf3 O-O 9. e3 Rfe8 10. Bb5 Rad8 11. Bxc6 bxc6 12. Ne5 Bc8 13. O-O Ba6 14. Re1 Bd6 15. Nxc6 Bxg3 16. Nxd8 Bxf2+ 17. Kxf2 Rxd8 18. b3 Ne4+ 19. Kg1 Nc3 20. Qd2 Ne4 21. Qa5 Bc8?? { (5.76 → Mate in 1) Checkmate is now unavoidable. Rf8 was best. } (21... Rf8 22. Qxa6 h5 23. Qf1 f5 24. c4 g5 25. Re2 f4 26. Qe1 fxe3 27. Rxe3) 22. Qxd8# { White wins by checkmate. } 1-0
"""
sample_multiple_games = """
[UTCDate "2024.06.06"]
[UTCTime "04:39:27"]

1. d4 e6 { A40 Horwitz Defense } 2. Bf4 c5 3. e3 cxd4 4. exd4 Nc6 5. Nf3 Nf6 6. c3 Qb6 7. Qb3 Qd8 8. Bd3 Be7 9. O-O O-O 10. Nbd2 d5 11. Rae1?! { (0.82 → 0.26) Inaccuracy. Qc2 was best. } (11. Qc2) 11... Nh5 12. Be3 Na5?! { (0.15 → 1.18) Inaccuracy. f5 was best. } (12... f5 13. Nb1 Nf6 14. Bf4 Ne4 15. h3 g5 16. Bh2 h5 17. c4 g4 18. Ne5) 13. Qc2 a6?? { (1.17 → 3.37) Blunder. f5 was best. } (13... f5 14. b4 Nc6 15. b5 Na5 16. c4 a6 17. a4 dxc4 18. Nxc4 axb5 19. axb5) 14. Bxh7+ Kh8 15. Bd3 b5 16. Ne5 Nf6 17. Kh1?! { (4.48 → 3.31) Inaccuracy. Bg5 was best. } (17. Bg5 Ng8 18. f4 Nh6 19. Bxh6 gxh6 20. Qd1 f5 21. Qh5 Rf6 22. g4 Bd7) 17... g6?! { (3.31 → 4.56) Inaccuracy. Nc4 was best. } (17... Nc4 18. Nc6 Qd6 19. Nxe7 Qxe7 20. Bg5 Qc7 21. Qc1 Nh7 22. Nf3 Kg8 23. Bf4) 18. Nef3? { (4.56 → 2.74) Mistake. Bh6 was best. } (18. Bh6 Qe8 19. Bxg6 fxg6 20. Qxg6 Qxg6 21. Nxg6+ Kh7 22. Bxf8 Bd8 23. Ne5 Nc4) 18... Kg7 19. Bg5 Rg8 20. Bxf6+?! { (2.63 → 1.78) Inaccuracy. Ne5 was best. } (20. Ne5 Qe8 21. f4 Nc4 22. Ndf3 Ra7 23. Nxf7 Kxf7 24. Ne5+ Kg7 25. Bxg6 Qf8) 20... Bxf6 21. Qd1 { White wins on time. } 1-0


[UTCDate "2024.06.02"]
[UTCTime "20:12:56"]

1. d4 d5 2. Nc3 { D00 Queen's Pawn Game: Chigorin Variation } Nc6 3. Bf4 Nf6?! { (0.15 → 0.72) Inaccuracy. a6 was best. } (3... a6 4. a3 Nf6 5. e3 Bf5 6. Bd3 Bxd3 7. Qxd3 e6 8. Nf3) 4. Nb5 e6?? { (0.66 → 3.76) Blunder. e5 was best. } (4... e5 5. Bxe5 Nxe5 6. dxe5 a6 7. Nc3 d4 8. exf6 dxc3 9. Qxd8+) 5. Nxc7+ Qxc7?! { (4.17 → 5.57) Inaccuracy. Kd7 was best. } (5... Kd7 6. Nxa8 Bd6 7. Bxd6 Kxd6 8. e3 Bd7 9. Bd3 Ke7 10. Qd2) 6. Bxc7 Bd7 7. Bg3 Be7 8. Nf3 O-O 9. e3 Rfe8 10. Bb5 Rad8 11. Bxc6 bxc6 12. Ne5 Bc8 13. O-O Ba6 14. Re1 Bd6 15. Nxc6 Bxg3 16. Nxd8 Bxf2+ 17. Kxf2 Rxd8 18. b3 Ne4+ 19. Kg1 Nc3 20. Qd2 Ne4 21. Qa5 Bc8?? { (5.76 → Mate in 1) Checkmate is now unavoidable. Rf8 was best. } (21... Rf8 22. Qxa6 h5 23. Qf1 f5 24. c4 g5 25. Re2 f4 26. Qe1 fxe3 27. Rxe3) 22. Qxd8# { White wins by checkmate. } 1-0
"""


def test_find_mistakes_in_one_game() -> None:
    with io.StringIO(sample_one_game) as pgn:
        actual = list(find_mistakes_in_one_game(pgn))
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
        assert actual[i].timestamp in expected_timestamps
        assert actual[i].fen in expected_fens
        assert actual[i].solution in expected_solutions
        expected_timestamps.remove(actual[i].timestamp)
        expected_fens.remove(actual[i].fen)
        expected_solutions.remove(actual[i].solution)
    assert len(expected_timestamps) == 0
    assert len(expected_fens) == 0
    assert len(expected_solutions) == 0


def test_find_all_mistakes() -> None:
    with io.StringIO(sample_multiple_games) as pgn:
        actual = list(find_all_mistakes(pgn))

    expected_timestamps = [
        1717648767000,
        1717648767000,
        1717648767000,
        1717648767000,
        1717648767000,
        1717648767000,
        1717648767000,
        1717359176000,
        1717359176000,
        1717359176000,
        1717359176000,
    ]
    expected_fens = [
        "r1bq1rk1/pp2bppp/2n1pn2/3p4/3P1B2/1QPB1N2/PP1N1PPP/R4RK1 w - - 0 11",
        "r1bq1rk1/pp2bppp/2n1p3/3p3n/3P4/1QPBBN2/PP1N1PPP/4RRK1 b - - 3 12",
        "r1bq1rk1/pp2bppp/4p3/n2p3n/3P4/2PBBN2/PPQN1PPP/4RRK1 b - - 5 13",
        "r1bq1r1k/4bpp1/p3pn2/np1pN3/3P4/2PBB3/PPQN1PPP/4RRK1 w - - 2 17",
        "r1bq1r1k/4bpp1/p3pn2/np1pN3/3P4/2PBB3/PPQN1PPP/4RR1K b - - 3 17",
        "r1bq1r1k/4bp2/p3pnp1/np1pN3/3P4/2PBB3/PPQN1PPP/4RR1K w - - 0 18",
        "r1bq2r1/4bpk1/p3pnp1/np1p2B1/3P4/2PB1N2/PPQN1PPP/4RR1K w - - 4 20",
        "r1bqkbnr/ppp1pppp/2n5/3p4/3P1B2/2N5/PPP1PPPP/R2QKBNR b KQkq - 3 3",
        "r1bqkb1r/ppp1pppp/2n2n2/1N1p4/3P1B2/8/PPP1PPPP/R2QKBNR b KQkq - 5 4",
        "r1bqkb1r/ppN2ppp/2n1pn2/3p4/3P1B2/8/PPP1PPPP/R2QKBNR b KQkq - 0 5",
        "3r2k1/p4ppp/b3p3/Q2p4/3Pn3/1P2P3/P1P3PP/R3R1K1 b - - 6 21",
    ]
    expected_solutions = [
        "b3c2",
        "f7f5",
        "f7f5",
        "e3g5",
        "a5c4",
        "e3h6",
        "f3e5",
        "a7a6",
        "e7e5",
        "e8d7",
        "d8f8",
    ]

    for i in range(len(actual)):
        assert actual[i].timestamp in expected_timestamps
        assert actual[i].fen in expected_fens
        assert actual[i].solution in expected_solutions
        expected_timestamps.remove(actual[i].timestamp)
        expected_fens.remove(actual[i].fen)
        expected_solutions.remove(actual[i].solution)
    assert len(expected_timestamps) == 0
    assert len(expected_fens) == 0
    assert len(expected_solutions) == 0
