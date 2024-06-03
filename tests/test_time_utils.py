from src.time_utils import convert_utc_to_unix


def test_convert_utc_to_unix() -> None:
    assert convert_utc_to_unix("2024.06.02", "20:12:56") == 1717359176000
