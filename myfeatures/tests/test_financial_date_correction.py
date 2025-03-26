import pytest
import sys
from datetime import date
import holidays

from myfeatures.dates import financial_date_correction

HOLIDAYS = holidays.financial_holidays("NYSE")


def test_date_is_valid_trading_date() -> None:
    today = date(year=2025, month=3, day=14)
    assert today == financial_date_correction(today, HOLIDAYS)


def test_date_is_on_weekend() -> None:
    today = date(year=2025, month=3, day=15)
    assert date(year=2025, month=3, day=14) == financial_date_correction(
        today, HOLIDAYS
    )


def test_date_is_on_holiday() -> None:
    today = date(year=2025, month=1, day=20)
    assert date(year=2025, month=1, day=17) == financial_date_correction(
        today, HOLIDAYS
    )


if __name__ == "__main__":
    pytest.main(sys.argv)
