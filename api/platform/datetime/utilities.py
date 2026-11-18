from datetime import datetime, timezone


def from_iso_string(iso_string: str) -> datetime:
    """
    Convert a UTC datetime string to a timezone-aware UTC datetime.

    The returned datetime is normalized to UTC and has microseconds removed,
    so it is safe to serialize as ISO 8601 with second precision.

    Args:
        iso_string (str): Datetime string in UTC, with second precision.

    Returns:
        datetime: A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.fromisoformat(iso_string).replace(tzinfo=timezone.utc, microsecond=0)


def from_timestamp(timestamp: int) -> datetime:
    """
    Convert a Unix timestamp to a timezone-aware UTC datetime.

    The returned datetime is normalized to UTC and has microseconds removed,
    so it is safe to serialize as ISO 8601 with second precision.

    Args:
        timestamp (int): Unix timestamp in seconds.

    Returns:
       (datetime): A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0)


def now() -> datetime:
    """
    Return the current UTC datetime with second precision.

    The returned datetime is timezone-aware, uses UTC, and has microseconds
    removed so it can be serialized consistently in ISO 8601 format.

    Returns:
        (datetime): A timezone-aware datetime in UTC with microseconds set to 0.
    """
    return datetime.now(timezone.utc).replace(microsecond=0)


def to_iso_string(dt: datetime) -> str:
    """
    Convert a datetime to an ISO 8601 UTC string with second precision.

    The datetime is first normalized to UTC, then truncated to whole seconds.

    Args:
        dt (datetime): A datetime object, timezone-aware or naive.

    Returns:
        str: An ISO 8601 formatted UTC string with second precision.
    """
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()
