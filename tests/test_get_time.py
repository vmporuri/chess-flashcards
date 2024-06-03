from src.get_time import convert_utc_to_unix


def test_convert_utc_to_unix():
    assert convert_utc_to_unix("2024.06.02", "20:12:56") == 1717359176000
