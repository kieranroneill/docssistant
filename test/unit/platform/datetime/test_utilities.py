from datetime import datetime, timedelta, timezone

import pytest

from api.platform.datetime.utilities import from_iso_string, to_iso_string


class TestFromISOString:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (
                "2023-01-01T00:00:00+00:00",
                datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc),
            ),
            (
                "2023-01-01T01:00:00+01:00",
                datetime(2023, 1, 1, 1, 0, tzinfo=timezone.utc),
            ),
            (
                "2023-01-01T00:00:10+00:00",
                datetime(2023, 1, 1, 0, 0, 10, tzinfo=timezone.utc),
            ),
            (
                "2023-01-01T00:00:00.123456+00:00",
                datetime(2023, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc),
            ),
        ],
    )
    def test_from_iso_string(self, value: str, expected: datetime) -> None:
        assert from_iso_string(value) == expected

    def test_from_iso_string_sets_utc_tzinfo(self) -> None:
        value = from_iso_string("2023-01-01T00:00:00+01:00")

        assert value.tzinfo == timezone.utc


class TestToISOString:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (datetime(2023, 1, 1, 0, 0, tzinfo=timezone.utc), "2023-01-01T00:00:00+00:00"),
            (datetime(2023, 1, 1, 1, 0, tzinfo=timezone(timedelta(hours=1))), "2023-01-01T00:00:00+00:00"),
        ],
    )
    def test_to_iso_string(self, value, expected):
        assert to_iso_string(value) == expected
