import datetime


def convert_utc_to_unix(date: str, time: str) -> int:
    """Given DATE and TIME strings, returns the Unix timestamp in milliseconds."""
    return 1000 * int(
        datetime.datetime.strptime(date + time, "%Y.%m.%d%H:%M:%S")
        .replace(tzinfo=datetime.timezone.utc)
        .timestamp()
    )
