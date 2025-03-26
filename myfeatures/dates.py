from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import holidays
from typing import Literal

HOLIDAYS = holidays.financial_holidays("NYSE")


class InvalidInputError(Exception):
    """Specific exception example."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def financial_date_correction(
    start_date: date,
    my_holidays: dict[datetime, str] = HOLIDAYS,
    direction: Literal["back", "forward"] = "back",
    last_weekday_num: int = 4,
) -> date:
    """If the date is on a holiday or weekend, it is pushed
    back/forward a day until it equals a valid trading date

    Args:
        start_date (date): original start date
        my_holidays (dict[datetime, str]): financial holdays

    Returns:
        date: corrected start date that does not land on holidays or weekends.
    """
    corrected_date = start_date  # modified date
    while corrected_date in my_holidays or corrected_date.weekday() > last_weekday_num:
        if direction == "back":
            corrected_date -= relativedelta(days=1)
        elif direction == "forward":
            corrected_date += relativedelta(days=1)
        else:
            raise InvalidInputError("direction input variable set to an invalid value")

    return corrected_date
